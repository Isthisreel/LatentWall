---
name: Odyssey ML SDK
description: Expert guidance for working with Odyssey ML's world model API for video generation, streaming, and simulation
---

# Odyssey ML SDK Skill

This skill provides comprehensive patterns and best practices for building applications with the Odyssey ML API, a multimodal world model for video generation.

## Prerequisites

**CRITICAL REQUIREMENTS:**
- Python 3.12 or higher (hard requirement)
- Odyssey API key (starts with `ody_`)
- SDK version ^1.0.0

## Installation

```bash
# Install from GitHub (not on PyPI yet)
pip install git+https://github.com/odysseyml/odyssey-python.git

# Or with uv
uv pip install git+https://github.com/odysseyml/odyssey-python.git
```

## Authentication

The SDK supports two authentication methods:

### Method 1: Environment Variable (Recommended)
```bash
export ODYSSEY_API_KEY=ody_your_api_key_here
```

### Method 2: Direct Initialization
```python
from odyssey import Odyssey

client = Odyssey(api_key="ody_your_api_key_here")
```

**Error Handling:**
- Invalid/missing key → `OdysseyAuthError`
- Connection issues → `OdysseyConnectionError`

## Core Architecture Patterns

### 1. Interactive Streaming (Real-Time)

Use for live, interactive video generation with user input.

```python
import asyncio
from odyssey import Odyssey, VideoFrame, OdysseyConnectionError

async def interactive_stream():
    client = Odyssey(api_key="ody_your_key")
    
    try:
        # Connect with callbacks
        await client.connect(
            on_connected=lambda: print("Connected!"),
            on_video_frame=lambda frame: process_frame(frame),
            on_stream_started=lambda sid: print(f"Stream: {sid}"),
            on_error=lambda err, fatal: print(f"Error: {err}")
        )
        
        # Start stream (returns stream_id)
        stream_id = await client.start_stream(
            prompt="A serene mountain landscape",
            portrait=True  # 704x1280, False for 1280x704
        )
        
        # Interact in real-time
        await asyncio.sleep(3)
        await client.interact("Add a waterfall")
        
        await asyncio.sleep(5)
        await client.end_stream()
        
    except OdysseyConnectionError as e:
        print(f"Connection failed: {e}")
        
    finally:
        # ALWAYS disconnect to free resources
        await client.disconnect()

def process_frame(frame: VideoFrame):
    # frame.data is np.ndarray (RGB uint8)
    # frame.width, frame.height, frame.timestamp_ms
    print(f"Frame: {frame.width}x{frame.height}")
```

### 2. Image-to-Video Generation

**Verified Feature:** Start video from an existing image.

```python
async def image_to_video():
    client = Odyssey(api_key="ody_your_key")
    
    try:
        await client.connect(on_video_frame=lambda f: None)
        
        # Method 1: File path
        stream_id = await client.start_stream(
            prompt="A cat playing",
            image="/path/to/cat.jpg"
        )
        
        # Method 2: PIL Image
        from PIL import Image
        pil_img = Image.open("/path/to/cat.jpg")
        stream_id = await client.start_stream(
            prompt="A cat playing",
            image=pil_img
        )
        
        # Method 3: NumPy array
        import numpy as np
        numpy_img = np.array(pil_img)
        stream_id = await client.start_stream(
            prompt="A cat playing",
            image=numpy_img
        )
        
        # Method 4: Raw bytes
        with open("/path/to/cat.jpg", "rb") as f:
            stream_id = await client.start_stream(
                prompt="A cat playing",
                image=f.read()
            )
        
        await asyncio.sleep(10)
        await client.end_stream()
        
    finally:
        await client.disconnect()
```

**Image Constraints:**
- Max size: 25 MB
- Formats: JPEG, PNG, WebP, GIF, BMP, HEIC, HEIF, AVIF
- Auto-resized to 1280x704 (landscape) or 704x1280 (portrait)

### 3. Simulate API (Batch Processing)

Use for pre-scripted sequences, batch generation, or background tasks.

```python
async def batch_simulation():
    client = Odyssey(api_key="ody_your_key")
    
    # Define script with timestamps
    script = [
        {
            "timestamp_ms": 0,
            "start": {
                "prompt": "A robot dancing in a neon city",
                "image": None  # Optional: add image path/data
            }
        },
        {
            "timestamp_ms": 5000,  # 5 seconds
            "interact": {
                "prompt": "The robot starts breakdancing"
            }
        },
        {
            "timestamp_ms": 10000,  # 10 seconds
            "end": {}
        }
    ]
    
    # Submit job (non-blocking)
    job = await client.simulate(script=script, portrait=True)
    print(f"Job submitted: {job.job_id}")
    
    # Poll for completion
    while True:
        await asyncio.sleep(5)
        status = await client.get_simulate_status(job.job_id)
        print(f"Status: {status.status}")
        
        if status.status not in ("pending", "running"):
            break
    
    # Retrieve results
    if status.status == "completed":
        for stream in status.streams:
            recording = await client.get_recording(stream.stream_id)
            print(f"Video: {recording.video_url}")
            print(f"Thumbnail: {recording.thumbnail_url}")
            print(f"Events: {recording.events_url}")
    else:
        print(f"Failed: {status.error_message}")
```

**Script Actions:**
- `start`: Initialize stream with prompt/image
- `interact`: Send new prompt during stream
- `end`: Terminate stream

### 4. Headless Processing (ML Workflows)

Collect frames without UI for ML pipelines.

```python
async def headless_processing():
    frames = []
    
    def collect_frame(frame: VideoFrame):
        # Copy to avoid overwriting
        frames.append(frame.data.copy())
    
    client = Odyssey(api_key="ody_your_key")
    
    try:
        await client.connect(on_video_frame=collect_frame)
        await client.start_stream("A busy city street")
        
        await asyncio.sleep(10)
        await client.end_stream()
        
    finally:
        await client.disconnect()
    
    print(f"Collected {len(frames)} frames")
    
    # Process with ML model
    # for frame in frames:
    #     predictions = model.predict(frame)
```

### 5. Recording Management

Retrieve generated videos and metadata.

```python
async def get_recordings():
    client = Odyssey(api_key="ody_your_key")
    
    # Get specific recording
    recording = await client.get_recording(stream_id="abc123")
    
    # URLs valid for ~1 hour
    print(f"Video (MP4): {recording.video_url}")
    print(f"Thumbnail (JPEG): {recording.thumbnail_url}")
    print(f"Events (JSONL): {recording.events_url}")
    
    # List all recordings (paginated)
    recordings_list = await client.list_stream_recordings(
        limit=20,
        offset=0
    )
    
    for rec in recordings_list.recordings:
        print(f"Stream {rec.stream_id}: {rec.video_url}")
```

## VideoFrame Processing

The `VideoFrame` object provides raw video data:

```python
class VideoFrame:
    data: np.ndarray  # RGB uint8 array (H, W, 3)
    width: int
    height: int
    timestamp_ms: int

# Integration with other libraries
def process_frame(frame: VideoFrame):
    # OpenCV
    import cv2
    bgr_frame = cv2.cvtColor(frame.data, cv2.COLOR_RGB2BGR)
    cv2.imshow("Odyssey Stream", bgr_frame)
    
    # PIL
    from PIL import Image
    pil_img = Image.fromarray(frame.data)
    pil_img.save(f"frame_{frame.timestamp_ms}.jpg")
    
    # NumPy processing
    grayscale = frame.data.mean(axis=2)
```

## Error Handling Best Practices

```python
from odyssey import (
    Odyssey,
    OdysseyAuthError,
    OdysseyConnectionError,
    OdysseyStreamError
)

async def robust_client():
    client = Odyssey(api_key="ody_your_key")
    
    try:
        await client.connect(
            on_error=lambda err, fatal: handle_error(err, fatal)
        )
        
        await client.start_stream("A cat")
        
    except OdysseyAuthError:
        print("Authentication failed - check API key")
        
    except OdysseyConnectionError as e:
        print(f"Connection failed: {e}")
        # Possible reasons:
        # - No streamers available
        # - Timed out waiting for streamer (default 30s)
        
    except OdysseyStreamError as e:
        print(f"Stream error: {e}")
        # Cannot interact when disconnected
        
    finally:
        try:
            await client.disconnect()
        except:
            pass  # Already disconnected

def handle_error(error: Exception, fatal: bool):
    if fatal:
        print(f"FATAL ERROR: {error}")
        # Must reconnect or exit
    else:
        print(f"Recoverable error: {error}")
        # Can continue
```

## Common Pitfalls

❌ **DON'T:**
- Use Python < 3.12
- Forget to call `disconnect()` in finally block
- Try to interact when disconnected
- Use interactive API for long-running batch tasks
- Assume recording URLs are permanent (1-hour expiry)
- Upload images > 25 MB

✅ **DO:**
- Always use try/finally for resource cleanup
- Use simulate API for batch/background tasks
- Use interactive API for real-time user interaction
- Copy frame data if storing (`frame.data.copy()`)
- Handle "no streamers available" errors gracefully
- Poll simulate status with reasonable intervals (5s+)

## Integration Patterns

### With OpenCV (Display Stream)

```python
import cv2

class OdysseyViewer:
    def __init__(self, client: Odyssey):
        self.client = client
        
    async def run(self, prompt: str):
        await self.client.connect(on_video_frame=self.display_frame)
        await self.client.start_stream(prompt)
        
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            await asyncio.sleep(0.1)
        
        await self.client.end_stream()
        await self.client.disconnect()
        cv2.destroyAllWindows()
    
    def display_frame(self, frame: VideoFrame):
        bgr = cv2.cvtColor(frame.data, cv2.COLOR_RGB2BGR)
        cv2.imshow("Odyssey", bgr)
```

### With FastAPI (HTTP Streaming)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/generate")
async def generate_video(prompt: str):
    client = Odyssey(api_key="ody_your_key")
    
    async def stream_frames():
        try:
            await client.connect(on_video_frame=lambda f: None)
            stream_id = await client.start_stream(prompt)
            await asyncio.sleep(10)
            await client.end_stream()
            
            recording = await client.get_recording(stream_id)
            yield recording.video_url
            
        finally:
            await client.disconnect()
    
    return StreamingResponse(stream_frames())
```

## Performance Tips

1. **Reuse Client**: Create one `Odyssey` instance per session
2. **Batch with Simulate**: Use simulate API for multiple non-interactive videos
3. **Frame Processing**: Process frames asynchronously to avoid blocking
4. **Queue Management**: Default timeout is 30s, adjust if needed
5. **Recording Retrieval**: Cache URLs but refresh before 1-hour expiry

## References

- Official Docs: https://documentation.api.odyssey.ml/
- GitHub: https://github.com/odysseyml/odyssey-python
- Python SDK: https://documentation.api.odyssey.ml/sdk/python/introduction
- API Reference: https://documentation.api.odyssey.ml/
