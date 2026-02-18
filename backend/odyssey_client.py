"""
Odyssey Client for Synesthesia Engine

Simplified client wrapper for generating visuals via Odyssey API.
"""

import os
import asyncio
from typing import Optional, Dict
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

from odyssey import (
    Odyssey,
    OdysseyAuthError,
    OdysseyConnectionError,
    OdysseyStreamError
)

logger = logging.getLogger(__name__)


class OdysseyClient:
    """Simplified Odyssey API client for visual generation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Odyssey client.
        
        Args:
            api_key: Odyssey API key (starts with 'ody_')
        """
        self.api_key = api_key or os.getenv("ODYSSEY_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "ODYSSEY_API_KEY not found. Set it in .env file or pass directly."
            )
        
        if not self.api_key.startswith("ody_"):
            raise ValueError("API key must start with 'ody_'")
        
        self.client = Odyssey(api_key=self.api_key)
        self.current_job_id: Optional[str] = None
        
        logger.info(f"Odyssey client initialized with key: {self.api_key[:8]}...")
    
    async def generate_scene(self, prompt: str, portrait: bool = False) -> Dict:
        """
        Generate a scene using Odyssey simulate API.
        
        Args:
            prompt: Text description of the scene
            portrait: Whether to use portrait orientation
            
        Returns:
            Dictionary with job_id and status
        """
        try:
            logger.info(f"Generating scene: {prompt[:100]}...")
            
            # Use simulate API for stateless generation
            # Correct format: [{"timestamp_ms": 0, "start": {"prompt": "..."}}, {"timestamp_ms": 5000, "end": {}}]
            job_detail = await self.client.simulate(
                script=[
                    {"timestamp_ms": 0, "start": {"prompt": prompt}},
                    {"timestamp_ms": 5000, "end": {}}  # 5 second video
                ],
                portrait=portrait
            )
            
            # Extract job_id from SimulationJobDetail object
            job_id = job_detail.job_id
            
            self.current_job_id = job_id
            
            logger.info(f"Generation started. Job ID: {job_id}")
            
            return {
                "job_id": job_id,
                "status": "processing",
                "prompt": prompt
            }
            
        except OdysseyAuthError as e:
            logger.error(f"Authentication failed: {e}")
            raise
        except OdysseyConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            raise
    
    async def get_job_status(self, job_id: Optional[str] = None) -> Dict:
        """
        Check status of a generation job.
        
        Args:
            job_id: Job ID to check (uses current if not provided)
            
        Returns:
            Dictionary with status and video URL if complete
        """
        job_id = job_id or self.current_job_id
        
        if not job_id:
            raise ValueError("No job ID provided or stored")
        
        try:
            status = await self.client.get_simulate_status(job_id)
            
            # status is a SimulationJobDetail object
            # status.status is a SimulationJobStatus enum
            # video_url is in status.streams[0].video_url
            
            result = {
                "job_id": job_id,
                "status": status.status.value,  # Convert enum to string
            }
           
            # Check if completed and has streams
            if status.status.value == "completed" and status.streams and len(status.streams) > 0:
                stream = status.streams[0]
                if stream.video_url:
                    result["video_url"] = stream.video_url
                    result["thumbnail_url"] = stream.thumbnail_url
                    result["stream_id"] = stream.stream_id
                    logger.info(f"Job {job_id} complete. URL: {stream.video_url}")
            elif status.status.value == "failed":
                result["error"] = status.error_message
                logger.error(f"Job {job_id} failed: {status.error_message}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error checking job status: {e}", exc_info=True)
            return {
                "job_id": job_id,
                "status": "error",
                "error": str(e)
            }
    
    async def connect(self, on_frame=None):
        """
        Connect to Odyssey platform.
        
        Args:
            on_frame: Callback for when a video frame is received
        """
        try:
            logger.info("Connecting to Odyssey...")
            await self.client.connect(
                on_video_frame=on_frame,
                on_error=lambda e, fatal: logger.error(f"Odyssey Error: {e} (fatal: {fatal})"),
                on_stream_error=lambda r, m: logger.error(f"Odyssey Stream Error: {r} - {m}")
            )
            logger.info("✅ Connected to Odyssey")
        except Exception as e:
            logger.error(f"Failed to connect to Odyssey: {e}")
            raise

    async def disconnect(self):
        """Disconnect from Odyssey."""
        await self.client.disconnect()
        logger.info("Disconnected from Odyssey")

    async def start_stream(self, prompt: str, portrait: bool = True):
        """
        Start an interactive stream.
        
        Args:
            prompt: Initial prompt
            portrait: Aspect ratio
        """
        try:
            logger.info(f"Starting interactive stream: {prompt}")
            await self.client.start_stream(prompt, portrait=portrait)
            logger.info("✅ Stream started")
        except Exception as e:
            logger.error(f"Failed to start stream: {e}")
            raise

    async def interact(self, prompt: str):
        """
        Send a new prompt to morph the active stream.
        
        Args:
            prompt: New prompt
        """
        try:
            logger.info(f"Interacting with stream: {prompt}")
            await self.client.interact(prompt)
            logger.debug("✅ Interaction sent")
        except Exception as e:
            logger.error(f"Failed to interact: {e}")
            raise

    async def end_stream(self):
        """End the active stream."""
        try:
            logger.info("Ending stream")
            await self.client.end_stream()
            logger.info("✅ Stream ended")
        except Exception as e:
            logger.error(f"Failed to end stream: {e}")
            raise
