"""
Synesthesia Engine - FastAPI Backend

Real-time audio-to-visual generation using Odyssey API.
"""

import json
import logging
import os
import io
import asyncio
import time
import base64
from pathlib import Path
from typing import Dict, Optional, List
from PIL import Image
import numpy as np

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from audio_processor import AudioProcessor, map_features_to_prompt
from odyssey_client import OdysseyClient, OdysseyAuthError, OdysseyConnectionError
from speech.keyword_extractor import KeywordExtractor

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Synesthesia Engine API",
    description="Audio-reactive visual generation with Odyssey",
    version="1.0.0"
)

# CORS configuration - Allow all for PoC stability
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load lore configuration
LORE_CONFIG_PATH = Path(__file__).parent / "lore_config.json"
with open(LORE_CONFIG_PATH, "r") as f:
    LORE_CONFIG = json.load(f)
    logger.info("Loaded Dino 26 lore configuration")

@app.get("/status")
async def get_status():
    """Health check for backend connectivity."""
    return {"status": "ok", "client_ready": odyssey_client is not None}

# Initialize components
audio_processor = AudioProcessor()
odyssey_client = None
keyword_extractor = KeywordExtractor()

class StreamManager:
    """Manages active WebSockets for real-time video streaming."""
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.is_streaming = False

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Video client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Video client disconnected. Total: {len(self.active_connections)}")

    async def broadcast_frame(self, frame_data_base64: str):
        """Broadcast a base64 encoded JPEG frame to all clients."""
        if not self.active_connections:
            return
            
        message = json.dumps({
            "type": "frame",
            "data": frame_data_base64
        })
        
        # Create a list of tasks for broadcasting
        tasks = []
        for connection in self.active_connections:
            tasks.append(connection.send_text(message))
            
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

stream_manager = StreamManager()
turbo_mode = True  # Enable Turbo Mode by default for speed

frame_count = 0

def on_odyssey_frame(frame):
    """Callback for Odyssey video frames."""
    global frame_count
    try:
        t_start = time.perf_counter()
        frame_count += 1
        if frame_count % 30 == 0:
            # We don't log every frame to keep logs clean, but we track processing time
            pass
            
        # Convert numpy array to PIL Image
        img = Image.fromarray(frame.data)
        
        # SUPER TURBO MODE: Extreme down-scale (1/4 size linearly, 1/16 size area)
        if turbo_mode:
            w, h = img.size
            img = img.resize((w // 4, h // 4), Image.NEAREST)
            
        # Save to buffer as JPEG with adaptive quality
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=50 if turbo_mode else 80)
        
        # Convert to base64
        frame_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        t_proc = (time.perf_counter() - t_start) * 1000
        if frame_count % 30 == 0:
            msg = f"🎥 Frame {frame_count} | Processing: {t_proc:.1f}ms | Clients: {len(stream_manager.active_connections)} | Turbo: {turbo_mode}\n"
            logger.info(msg.strip())
            latency_file = Path(__file__).parent / "latency.txt"
            with open(latency_file, "a", encoding="utf-8") as f:
                f.write(msg)
                f.flush() # Ensure it written immediately

        # Broadcast to WebSockets (run in event loop)
        asyncio.run_coroutine_threadsafe(
            stream_manager.broadcast_frame(frame_base64),
            asyncio.get_event_loop()
        )
    except Exception as e:
        logger.error(f"Error encoding frame: {e}")

try:
    odyssey_client = OdysseyClient()
    logger.info("✅ Odyssey client initialized successfully")
except Exception as e:
    logger.warning(f"⚠️ Odyssey client initialization failed: {e}")
    odyssey_client = None

# Internal benchmark function to capture "Real Numbers" alone
async def run_benchmark():
    if not odyssey_client or not stream_manager.is_streaming:
        logger.warning("🧪 Benchmark skipped: Odyssey client or stream not ready")
        return {"error": "Not ready"}
        
    logger.info("🧪 AUTO-BENCHMARK: Starting tests...")
    words = ["dragon", "forest", "storm", "cyberpunk", "nebula"]
    results = []
    for word in words:
        try:
            t_start = time.perf_counter()
            # Simulate speech input
            keywords = keyword_extractor.extract_keywords(word)
            prompt = keyword_extractor.build_prompt(keywords)
            t_nlp = (time.perf_counter() - t_start) * 1000
            
            t_int_start = time.perf_counter()
            await odyssey_client.interact(prompt)
            t_int = (time.perf_counter() - t_int_start) * 1000
            
            msg = f"📊 AUTO-TEST | Word: {word} | Mode: {'Turbo' if turbo_mode else 'Normal'} | NLP: {t_nlp:.1f}ms | AI-Int: {t_int:.1f}ms\n"
            latency_file = Path(__file__).parent / "latency.txt"
            with open(latency_file, "a", encoding="utf-8") as f:
                f.write(msg)
                f.flush()
            logger.info(msg.strip())
            results.append({"word": word, "nlp": t_nlp, "ai": t_int})
            
        except Exception as e:
            logger.error(f"Auto-benchmark step failed: {e}")
        await asyncio.sleep(3) # Space out tests
    logger.info("🏁 AUTO-BENCHMARK COMPLETED.")
    return results


# --- Pydantic Models ---

class GenerateRequest(BaseModel):
    """Request model for manual generation."""
    prompt: str
    portrait: bool = False


class JobStatusResponse(BaseModel):
    """Response model for job status."""
    job_id: str
    status: str
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    error: Optional[str] = None


class SpeechToVideoRequest(BaseModel):
    """Request model for speech-to-video."""
    text: str


class SpeechToVideoResponse(BaseModel):
    """Response model for speech-to-video."""
    job_id: str
    prompt: str
    keywords: list
    status: str = "processing"


# --- REST Endpoints ---

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "app": "Synesthesia Engine",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    odyssey_status = "connected" if odyssey_client else "disconnected"
    
    return {
        "status": "healthy",
        "odyssey": odyssey_status,
        "lore_loaded": bool(LORE_CONFIG)
    }


@app.get("/lore")
async def get_lore():
    """Get Dino 26 lore configuration."""
    return LORE_CONFIG


@app.post("/generate", response_model=JobStatusResponse)
async def generate_visual(request: GenerateRequest):
    """
    Generate visual from manual prompt.
    
    Args:
        request: Generation request with prompt
        
    Returns:
        Job status with job_id
    """
    if not odyssey_client:
        raise HTTPException(status_code=503, detail="Odyssey client not available")
    
    try:
        result = await odyssey_client.generate_scene(
            prompt=request.prompt,
            portrait=request.portrait
        )
        return JobStatusResponse(**result)
        
    except OdysseyAuthError:
        raise HTTPException(status_code=401, detail="Odyssey authentication failed")
    except OdysseyConnectionError:
        raise HTTPException(status_code=503, detail="Odyssey connection error")
    except Exception as e:
        logger.error(f"Generation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/job/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """
    Check status of a generation job.
    
    Args:
        job_id: Odyssey job ID
        
    Returns:
        Job status
    """
    if not odyssey_client:
        raise HTTPException(status_code=503, detail="Odyssey client not available")
    
    try:
        status = await odyssey_client.get_job_status(job_id)
        return JobStatusResponse(**status)
        
    except Exception as e:
        logger.error(f"Error checking job status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stream/start")
async def start_stream(request: GenerateRequest):
    """Start an interactive Odyssey stream."""
    if not odyssey_client:
        raise HTTPException(status_code=503, detail="Odyssey client not available")
    
    try:
        # Connect if not connected
        await odyssey_client.connect(on_frame=on_odyssey_frame)
        
        # Start stream
        await odyssey_client.start_stream(request.prompt, portrait=request.portrait)
        stream_manager.is_streaming = True
        
        return {"status": "started", "prompt": request.prompt}
    except Exception as e:
        logger.error(f"Stream start error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stream/end")
async def end_stream():
    """End the interactive Odyssey stream."""
    if not odyssey_client:
        raise HTTPException(status_code=503, detail="Odyssey client not available")
    
    try:
        await odyssey_client.end_stream()
        await odyssey_client.disconnect()
        stream_manager.is_streaming = False
        return {"status": "ended"}
    except Exception as e:
        logger.error(f"Stream end error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/benchmark")
async def trigger_benchmark():
    """Manually trigger the internal performance benchmark."""
    results = await run_benchmark()
    return {"status": "benchmark_completed", "results": results}


@app.post("/turbo")
async def toggle_turbo(enabled: bool):
    """Toggle Turbo Mode."""
    global turbo_mode
    turbo_mode = enabled
    logger.info(f"🚀 Turbo Mode set to: {turbo_mode}")
    return {"turbo_mode": turbo_mode}


@app.post("/speech-to-video", response_model=SpeechToVideoResponse)
async def speech_to_video(request: SpeechToVideoRequest):
    """
    Convert speech text to video via keyword extraction.
    
    WHAT DI U MEAN endpoint:
    1. Extract keywords from speech
    2. Build visual prompt
    3. Generate video
    
    Args:
        request: Speech text from browser
        
    Returns:
        Job ID and prompt
    """
    if not odyssey_client:
        raise HTTPException(status_code=503, detail="Odyssey client not available")
    
    try:
        t_start = time.perf_counter()
        
        # Extract keywords and build prompt
        keywords = keyword_extractor.extract_keywords(request.text)
        prompt = keyword_extractor.build_prompt(keywords)
        
        t_nlp = (time.perf_counter() - t_start) * 1000
        
        msg_nlp = f"Speech: '{request.text}' → Prompt: '{prompt}' (NLP: {t_nlp:.1f}ms)\n"
        logger.info(msg_nlp.strip())
        latency_file = Path(__file__).parent / "latency.txt"
        with open(latency_file, "a", encoding="utf-8") as f:
            f.write(msg_nlp)
            f.flush()
        
        # Use interaction if streaming, otherwise simulate
        if stream_manager.is_streaming:
            t_interact_start = time.perf_counter()
            await odyssey_client.interact(prompt)
            t_interact = (time.perf_counter() - t_interact_start) * 1000
            
            msg_int = f"⚡ Interaction acknowledged in {t_interact:.1f}ms\n"
            logger.info(msg_int.strip())
            with open(latency_file, "a", encoding="utf-8") as f:
                f.write(msg_int)
                f.flush()
            
            return SpeechToVideoResponse(
                job_id="interactive_stream",
                prompt=prompt,
                keywords=[{"word": w, "category": c} for w, c in keywords],
                status="streaming"
            )
        else:
            # Generate video (simulation mode)
            result = await odyssey_client.generate_scene(
                prompt=prompt,
                portrait=True  # Portrait for vertical display
            )
            
            return SpeechToVideoResponse(
                job_id=result['job_id'],
                prompt=prompt,
                keywords=[{"word": w, "category": c} for w, c in keywords],
                status=result['status']
            )
        
    except Exception as e:
        logger.error(f"Speech-to-video error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# --- WebSocket Endpoints ---

@app.websocket("/ws/video")
async def websocket_video(websocket: WebSocket):
    """WebSocket for real-time video frames."""
    await stream_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        stream_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Video WebSocket error: {e}")
        stream_manager.disconnect(websocket)


@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    """
    WebSocket endpoint for real-time audio streaming.
    
    Protocol:
    1. Client sends audio chunks (binary/blob)
    2. Server analyzes audio → extracts features
    3. Server maps features → lore config → prompt
    4. Server sends generation → Odyssey API
    5. Server returns → job status/video URL to client
    """
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    if not odyssey_client:
        await websocket.send_json({
            "type": "error",
            "message": "Odyssey client not available"
        })
        await websocket.close()
        return
    
    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "message": "Synesthesia Engine ready",
            "lore": LORE_CONFIG["project"]
        })
        
        while True:
            # Receive audio chunk
            data = await websocket.receive()
            
            if "bytes" in data:
                # Binary audio data
                audio_bytes = data["bytes"]
                logger.info(f"Received audio chunk: {len(audio_bytes)} bytes")
                
                # Step 1: Analyze audio
                features = audio_processor.process_chunk(audio_bytes)
                
                await websocket.send_json({
                    "type": "analysis",
                    "features": features
                })
                
                # Step 2: Map to lore configuration
                prompt = map_features_to_prompt(features, LORE_CONFIG)
                
                await websocket.send_json({
                    "type": "prompt",
                    "prompt": prompt,
                    "energy_level": audio_processor.classify_energy_level(features)
                })
                
                # Step 3: Generate with Odyssey
                result = await odyssey_client.generate_scene(
                    prompt=prompt,
                    portrait=False  # Landscape for immersive experience
                )
                
                await websocket.send_json({
                    "type": "generation_started",
                    "job_id": result["job_id"]
                })
                
                # Step 4: Poll for completion (async)
                # Note: In production, use background task or webhook
                status = await odyssey_client.wait_for_completion(
                    job_id=result["job_id"],
                    timeout=60,  # 1 minute timeout for PoC
                    poll_interval=3
                )
                
                await websocket.send_json({
                    "type": "generation_complete",
                    **status
                })
                
            elif "text" in data:
                # Text control messages
                message = json.loads(data["text"])
                logger.info(f"Received control message: {message}")
                
                if message.get("action") == "ping":
                    await websocket.send_json({"type": "pong"})
                
            else:
                logger.warning(f"Unknown data type: {data}")
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
        except:
            pass
    finally:
        logger.info("WebSocket connection closed")


# --- Startup Event ---

@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("🦖 Synesthesia Engine starting up...")
    logger.info(f"Lore: {LORE_CONFIG['project']}")
    logger.info(f"Themes: {', '.join(LORE_CONFIG['themes'])}")
    
    if odyssey_client:
        logger.info("✅ Odyssey client ready")
    else:
        logger.warning("⚠️ Odyssey client not initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("🛑 Synesthesia Engine shutting down...")


# --- Run with Uvicorn ---

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
