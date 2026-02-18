"""
Video Frame Processor

Utilities for processing VideoFrame objects from Odyssey streams.
Includes format conversion, file I/O, and buffering.
"""

import asyncio
from pathlib import Path
from typing import List, Optional
import numpy as np
from PIL import Image
import aiofiles
import structlog

try:
    import cv2
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False

from odyssey import VideoFrame

logger = structlog.get_logger()


class FrameCollector:
    """
    Collects video frames in memory with optional buffering.
    
    Example:
        >>> collector = FrameCollector(max_frames=300)
        >>> await client.connect(on_video_frame=collector.collect)
        >>> # ... after stream ...
        >>> frames = collector.get_frames()
    """
    
    def __init__(self, max_frames: Optional[int] = None):
        """
        Args:
            max_frames: Maximum frames to keep (oldest dropped), None = unlimited
        """
        self.max_frames = max_frames
        self.frames: List[np.ndarray] = []
        self.metadata: List[dict] = []
        self._lock = asyncio.Lock()
    
    def collect(self, frame: VideoFrame) -> None:
        """
        Callback for on_video_frame.
        
        Args:
            frame: VideoFrame from Odyssey
        """
        # Must copy to avoid data being overwritten
        frame_copy = frame.data.copy()
        
        metadata = {
            'width': frame.width,
            'height': frame.height,
            'timestamp_ms': frame.timestamp_ms
        }
        
        # Thread-safe append
        if self.max_frames and len(self.frames) >= self.max_frames:
            self.frames.pop(0)
            self.metadata.pop(0)
        
        self.frames.append(frame_copy)
        self.metadata.append(metadata)
        
        logger.debug(
            "Frame collected",
            total=len(self.frames),
            timestamp=frame.timestamp_ms
        )
    
    def get_frames(self) -> List[np.ndarray]:
        """Get all collected frames."""
        return self.frames.copy()
    
    def get_metadata(self) -> List[dict]:
        """Get metadata for all frames."""
        return self.metadata.copy()
    
    def clear(self) -> None:
        """Clear all collected frames."""
        self.frames.clear()
        self.metadata.clear()
        logger.info("Frames cleared")
    
    def __len__(self) -> int:
        return len(self.frames)


class FrameConverter:
    """Convert between different image formats."""
    
    @staticmethod
    def to_pil(frame: VideoFrame | np.ndarray) -> Image.Image:
        """
        Convert to PIL Image.
        
        Args:
            frame: VideoFrame or numpy array (RGB)
            
        Returns:
            PIL Image object
        """
        if isinstance(frame, VideoFrame):
            data = frame.data
        else:
            data = frame
        
        return Image.fromarray(data)
    
    @staticmethod
    def to_opencv(frame: VideoFrame | np.ndarray) -> np.ndarray:
        """
        Convert to OpenCV format (BGR).
        
        Args:
            frame: VideoFrame or numpy array (RGB)
            
        Returns:
            BGR numpy array for OpenCV
            
        Raises:
            ImportError: If opencv-python not installed
        """
        if not HAS_OPENCV:
            raise ImportError(
                "opencv-python not installed. "
                "Run: pip install opencv-python"
            )
        
        if isinstance(frame, VideoFrame):
            data = frame.data
        else:
            data = frame
        
        return cv2.cvtColor(data, cv2.COLOR_RGB2BGR)
    
    @staticmethod
    def from_file(filepath: str | Path) -> np.ndarray:
        """
        Load image from file as RGB numpy array.
        
        Args:
            filepath: Path to image file
            
        Returns:
            RGB numpy array
        """
        img = Image.open(filepath)
        return np.array(img.convert('RGB'))


class FrameSaver:
    """Save frames to disk."""
    
    def __init__(self, output_dir: str | Path = "./outputs"):
        """
        Args:
            output_dir: Directory for saved frames
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("FrameSaver initialized", output_dir=str(self.output_dir))
    
    async def save_frame(
        self,
        frame: VideoFrame | np.ndarray,
        filename: str,
        format: str = "JPEG"
    ) -> Path:
        """
        Save single frame to disk.
        
        Args:
            frame: VideoFrame or numpy array
            filename: Output filename (without extension)
            format: Image format (JPEG, PNG, etc.)
            
        Returns:
            Path to saved file
        """
        pil_img = FrameConverter.to_pil(frame)
        
        ext = format.lower()
        filepath = self.output_dir / f"{filename}.{ext}"
        
        # Save asynchronously
        await asyncio.to_thread(pil_img.save, filepath, format)
        
        logger.info("Frame saved", filepath=str(filepath))
        return filepath
    
    async def save_frames(
        self,
        frames: List[np.ndarray],
        prefix: str = "frame",
        format: str = "JPEG"
    ) -> List[Path]:
        """
        Save multiple frames.
        
        Args:
            frames: List of numpy arrays
            prefix: Filename prefix
            format: Image format
            
        Returns:
            List of saved file paths
        """
        tasks = [
            self.save_frame(frame, f"{prefix}_{i:05d}", format)
            for i, frame in enumerate(frames)
        ]
        
        paths = await asyncio.gather(*tasks)
        logger.info("Frames saved", count=len(paths))
        return paths


class VideoWriter:
    """Write frames to video file using OpenCV."""
    
    def __init__(
        self,
        output_path: str | Path,
        fps: int = 30,
        codec: str = 'mp4v'
    ):
        """
        Args:
            output_path: Path for output video
            fps: Frames per second
            codec: FourCC codec code
            
        Raises:
            ImportError: If opencv-python not installed
        """
        if not HAS_OPENCV:
            raise ImportError(
                "opencv-python required for video writing. "
                "Run: pip install opencv-python"
            )
        
        self.output_path = Path(output_path)
        self.fps = fps
        self.codec = cv2.VideoWriter_fourcc(*codec)
        self.writer: Optional[cv2.VideoWriter] = None
        self._initialized = False
        
        logger.info(
            "VideoWriter created",
            output=str(output_path),
            fps=fps
        )
    
    def write_frame(self, frame: VideoFrame | np.ndarray) -> None:
        """
        Write a single frame to video.
        
        Args:
            frame: VideoFrame or numpy array (RGB)
        """
        if isinstance(frame, VideoFrame):
            data = frame.data
            height, width = frame.height, frame.width
        else:
            data = frame
            height, width = data.shape[:2]
        
        # Initialize writer on first frame
        if not self._initialized:
            self.writer = cv2.VideoWriter(
                str(self.output_path),
                self.codec,
                self.fps,
                (width, height)
            )
            self._initialized = True
            logger.info("VideoWriter initialized", width=width, height=height)
        
        # Convert to BGR for OpenCV
        bgr_frame = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)
        self.writer.write(bgr_frame)
    
    def write_frames(self, frames: List[np.ndarray]) -> None:
        """
        Write multiple frames.
        
        Args:
            frames: List of numpy arrays (RGB)
        """
        for frame in frames:
            self.write_frame(frame)
        
        logger.info("Frames written", count=len(frames))
    
    def close(self) -> None:
        """Release video writer resources."""
        if self.writer is not None:
            self.writer.release()
            logger.info("VideoWriter closed", output=str(self.output_path))
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


async def save_stream_to_video(
    frames: List[np.ndarray],
    output_path: str | Path,
    fps: int = 30
) -> Path:
    """
    Convenience function to save frames as video.
    
    Args:
        frames: List of RGB numpy arrays
        output_path: Output video path
        fps: Frames per second
        
    Returns:
        Path to saved video
        
    Example:
        >>> collector = FrameCollector()
        >>> # ... collect frames ...
        >>> await save_stream_to_video(
        ...     collector.get_frames(),
        ...     "output.mp4"
        ... )
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with VideoWriter(output_path, fps=fps) as writer:
        writer.write_frames(frames)
    
    logger.info("Stream saved to video", output=str(output_path))
    return output_path


# Example integration
class StreamRecorder:
    """
    Complete stream recording solution.
    
    Records frames and automatically saves to video when done.
    
    Example:
        >>> recorder = StreamRecorder("output.mp4")
        >>> await client.connect(on_video_frame=recorder.on_frame)
        >>> await client.start_stream("A cat")
        >>> await asyncio.sleep(10)
        >>> await client.end_stream()
        >>> await recorder.finalize()
    """
    
    def __init__(
        self,
        output_path: str | Path,
        fps: int = 30,
        max_frames: Optional[int] = None
    ):
        self.output_path = Path(output_path)
        self.fps = fps
        self.collector = FrameCollector(max_frames=max_frames)
        logger.info("StreamRecorder initialized", output=str(output_path))
    
    def on_frame(self, frame: VideoFrame) -> None:
        """Callback for on_video_frame."""
        self.collector.collect(frame)
    
    async def finalize(self) -> Path:
        """
        Save collected frames to video.
        
        Returns:
            Path to saved video file
        """
        frames = self.collector.get_frames()
        
        if not frames:
            logger.warning("No frames to save")
            raise ValueError("No frames collected")
        
        logger.info("Finalizing recording", frame_count=len(frames))
        
        return await save_stream_to_video(
            frames,
            self.output_path,
            fps=self.fps
        )
