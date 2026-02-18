"""
Odyssey Client Wrapper

Provides a singleton client manager with automatic reconnection,
logging, and configuration management.
"""

import asyncio
import os
from pathlib import Path
from typing import Optional, Callable
from dotenv import load_dotenv
from odyssey import (
    Odyssey,
    VideoFrame,
    OdysseyAuthError,
    OdysseyConnectionError,
    OdysseyStreamError,
    ConnectionStatus
)

# Load .env file
load_dotenv()
import structlog

logger = structlog.get_logger()


class OdysseyClientManager:
    """
    Singleton manager for Odyssey client connections.
    
    This class ensures only one active connection exists and provides
    automatic reconnection logic and consistent error handling.
    """
    
    _instance: Optional['OdysseyClientManager'] = None
    _client: Optional[Odyssey] = None
    _connected: bool = False
    _current_stream_id: Optional[str] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize with API key from environment."""
        if not hasattr(self, 'initialized'):
            self.api_key = os.getenv('ODYSSEY_API_KEY')
            if not self.api_key:
                raise ValueError(
                    "ODYSSEY_API_KEY not found in environment. "
                    "Set it in .env file or export it."
                )
            self.initialized = True
            logger.info("OdysseyClientManager initialized", api_key_prefix=self.api_key[:8])
    
    @property
    def client(self) -> Odyssey:
        """Get or create Odyssey client instance."""
        if self._client is None:
            self._client = Odyssey(api_key=self.api_key)
            logger.info("Created new Odyssey client")
        return self._client
    
    @property
    def is_connected(self) -> bool:
        """Check if client is currently connected."""
        return self._connected
    
    @property
    def current_stream_id(self) -> Optional[str]:
        """Get the current active stream ID."""
        return self._current_stream_id
    
    async def connect(
        self,
        on_video_frame: Optional[Callable[[VideoFrame], None]] = None,
        on_stream_started: Optional[Callable[[str], None]] = None,
        on_stream_ended: Optional[Callable[[], None]] = None,
        on_error: Optional[Callable[[Exception, bool], None]] = None,
    ) -> None:
        """
        Connect to Odyssey streaming service.
        
        Args:
            on_video_frame: Callback for each video frame received
            on_stream_started: Callback when stream starts
            on_stream_ended: Callback when stream ends
            on_error: Callback for errors (error, is_fatal)
            
        Raises:
            OdysseyAuthError: If authentication fails
            OdysseyConnectionError: If connection fails
        """
        if self._connected:
            logger.warning("Already connected, skipping reconnection")
            return
        
        try:
            logger.info("Attempting to connect to Odyssey")
            
            await self.client.connect(
                on_connected=self._on_connected,
                on_disconnected=self._on_disconnected,
                on_video_frame=on_video_frame or self._default_frame_handler,
                on_stream_started=on_stream_started or self._on_stream_started,
                on_stream_ended=on_stream_ended or self._on_stream_ended,
                on_stream_error=self._on_stream_error,
                on_error=on_error or self._on_error,
                on_status_change=self._on_status_change,
            )
            
            self._connected = True
            logger.info("Successfully connected to Odyssey")
            
        except OdysseyAuthError as e:
            logger.error("Authentication failed", error=str(e))
            raise
            
        except OdysseyConnectionError as e:
            logger.error("Connection failed", error=str(e))
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from Odyssey and clean up resources."""
        if not self._connected:
            logger.warning("Not connected, skipping disconnect")
            return
        
        try:
            logger.info("Disconnecting from Odyssey")
            await self.client.disconnect()
            self._connected = False
            self._current_stream_id = None
            logger.info("Successfully disconnected")
            
        except Exception as e:
            logger.error("Error during disconnect", error=str(e))
            # Still mark as disconnected
            self._connected = False
            self._current_stream_id = None
    
    async def start_stream(
        self,
        prompt: str,
        portrait: bool = True,
        image: Optional[str | bytes] = None
    ) -> str:
        """
        Start a new video stream.
        
        Args:
            prompt: Text description for video generation
            portrait: If True, generate 704x1280, else 1280x704
            image: Optional image for image-to-video (path or bytes)
            
        Returns:
            stream_id: Unique identifier for the stream
            
        Raises:
            OdysseyStreamError: If not connected or stream fails
        """
        if not self._connected:
            raise OdysseyStreamError("Cannot start stream: client is not connected")
        
        logger.info(
            "Starting stream",
            prompt=prompt,
            portrait=portrait,
            has_image=image is not None
        )
        
        try:
            stream_id = await self.client.start_stream(
                prompt=prompt,
                portrait=portrait,
                image=image
            )
            
            self._current_stream_id = stream_id
            logger.info("Stream started", stream_id=stream_id)
            return stream_id
            
        except Exception as e:
            logger.error("Failed to start stream", error=str(e))
            raise
    
    async def interact(self, prompt: str) -> None:
        """
        Send interaction prompt to current stream.
        
        Args:
            prompt: New instruction for the video
            
        Raises:
            OdysseyStreamError: If not connected or no active stream
        """
        if not self._connected:
            raise OdysseyStreamError("Cannot interact: client is not connected")
        
        if not self._current_stream_id:
            raise OdysseyStreamError("Cannot interact: no active stream")
        
        logger.info("Sending interaction", prompt=prompt)
        
        try:
            await self.client.interact(prompt=prompt)
            logger.info("Interaction sent")
            
        except Exception as e:
            logger.error("Interaction failed", error=str(e))
            raise
    
    async def end_stream(self) -> None:
        """
        End the current stream.
        
        Raises:
            OdysseyStreamError: If not connected or no active stream
        """
        if not self._connected:
            raise OdysseyStreamError("Cannot end stream: client is not connected")
        
        if not self._current_stream_id:
            logger.warning("No active stream to end")
            return
        
        logger.info("Ending stream", stream_id=self._current_stream_id)
        
        try:
            await self.client.end_stream()
            logger.info("Stream ended", stream_id=self._current_stream_id)
            self._current_stream_id = None
            
        except Exception as e:
            logger.error("Failed to end stream", error=str(e))
            self._current_stream_id = None
            raise
    
    async def get_recording(self, stream_id: str):
        """
        Get recording URLs for a completed stream.
        
        Args:
            stream_id: ID of the completed stream
            
        Returns:
            Recording object with video_url, thumbnail_url, events_url
        """
        logger.info("Retrieving recording", stream_id=stream_id)
        
        try:
            recording = await self.client.get_recording(stream_id)
            logger.info(
                "Recording retrieved",
                stream_id=stream_id,
                has_video=bool(recording.video_url)
            )
            return recording
            
        except Exception as e:
            logger.error("Failed to get recording", stream_id=stream_id, error=str(e))
            raise
    
    # Internal event handlers
    
    def _on_connected(self) -> None:
        logger.info("Event: Connected to Odyssey")
    
    def _on_disconnected(self) -> None:
        logger.info("Event: Disconnected from Odyssey")
        self._connected = False
        self._current_stream_id = None
    
    def _on_stream_started(self, stream_id: str) -> None:
        logger.info("Event: Stream started", stream_id=stream_id)
        self._current_stream_id = stream_id
    
    def _on_stream_ended(self) -> None:
        logger.info("Event: Stream ended", stream_id=self._current_stream_id)
        self._current_stream_id = None
    
    def _on_stream_error(self, error_type: str, message: str) -> None:
        logger.error(
            "Event: Stream error",
            error_type=error_type,
            message=message,
            stream_id=self._current_stream_id
        )
    
    def _on_error(self, error: Exception, fatal: bool) -> None:
        if fatal:
            logger.error("Event: Fatal error", error=str(error))
            self._connected = False
        else:
            logger.warning("Event: Recoverable error", error=str(error))
    
    def _on_status_change(
        self,
        status: ConnectionStatus,
        message: Optional[str]
    ) -> None:
        logger.info(
            "Event: Status change",
            status=status.name,
            message=message
        )
    
    def _default_frame_handler(self, frame: VideoFrame) -> None:
        """Default frame handler - just logs receipt."""
        logger.debug(
            "Received frame",
            width=frame.width,
            height=frame.height,
            timestamp_ms=frame.timestamp_ms
        )


# Convenience function for common use case
async def quick_generate(
    prompt: str,
    duration: int = 10,
    portrait: bool = True,
    image: Optional[str] = None
) -> str:
    """
    Quick video generation with automatic cleanup.
    
    Args:
        prompt: Text description
        duration: How long to generate (seconds)
        portrait: Video orientation
        image: Optional image path
        
    Returns:
        stream_id: ID of the generated stream
        
    Example:
        >>> stream_id = await quick_generate("A cat playing", duration=5)
        >>> manager = OdysseyClientManager()
        >>> recording = await manager.get_recording(stream_id)
    """
    manager = OdysseyClientManager()
    
    try:
        await manager.connect()
        stream_id = await manager.start_stream(prompt, portrait, image)
        
        await asyncio.sleep(duration)
        await manager.end_stream()
        
        return stream_id
        
    finally:
        await manager.disconnect()
