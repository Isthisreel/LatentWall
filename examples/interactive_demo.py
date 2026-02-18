"""
Interactive Demo - Real-time streaming with Odyssey
"""

import asyncio
import argparse
import os
import logging
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from odyssey_client import OdysseyClientManager
from video_processor import StreamRecorder
import structlog

# Setup logging
structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(
        logging.INFO if not os.getenv('DEBUG') else logging.DEBUG
    )
)

logger = structlog.get_logger()


async def interactive_demo(
    prompt: str,
    duration: int = 10,
    portrait: bool = True,
    save_video: bool = False,
    output_path: str = None
):
    """
    Run interactive streaming demo.
    
    Args:
        prompt: Initial text prompt
        duration: How long to generate (seconds)
        portrait: Video orientation
        save_video: Whether to save video to file
        output_path: Path for saved video
    """
    manager = OdysseyClientManager()
    recorder = None
    
    if save_video:
        output_path = output_path or f"outputs/demo_{asyncio.get_event_loop().time()}.mp4"
        recorder = StreamRecorder(output_path)
        logger.info("Recording enabled", output=output_path)
    
    try:
        logger.info("Connecting to Odyssey...")
        
        await manager.connect(
            on_video_frame=recorder.on_frame if recorder else None
        )
        
        logger.info("Starting stream", prompt=prompt)
        stream_id = await manager.start_stream(
            prompt=prompt,
            portrait=portrait
        )
        
        logger.info(
            f"Stream started! Generating for {duration} seconds...",
            stream_id=stream_id
        )
        
        # Let it run
        await asyncio.sleep(duration)
        
        logger.info("Ending stream...")
        await manager.end_stream()
        
        # Get recording info
        recording = await manager.get_recording(stream_id)
        logger.info(
            "Recording available",
            video_url=recording.video_url,
            thumbnail_url=recording.thumbnail_url
        )
        
        print(f"\n✅ SUCCESS!")
        print(f"Stream ID: {stream_id}")
        print(f"Video URL: {recording.video_url}")
        print(f"⚠️  URLs expire in ~1 hour")
        
        if recorder:
            saved_path = await recorder.finalize()
            print(f"Saved to: {saved_path}")
        
    except Exception as e:
        logger.error("Demo failed", error=str(e))
        raise
        
    finally:
        await manager.disconnect()
        logger.info("Demo complete")


async def test_connection():
    """Test Odyssey connection and authentication."""
    manager = OdysseyClientManager()
    
    try:
        logger.info("Testing connection...")
        await manager.connect()
        logger.info("✅ Connection successful!")
        
        await manager.disconnect()
        print("\n✅ Authentication and connection test passed!")
        
    except Exception as e:
        logger.error("❌ Connection test failed", error=str(e))
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Odyssey Interactive Demo"
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        default="A serene mountain landscape with a waterfall",
        help="Text prompt for video generation"
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        default=10,
        help="Duration in seconds"
    )
    
    parser.add_argument(
        '--portrait',
        action='store_true',
        help="Generate portrait video (704x1280)"
    )
    
    parser.add_argument(
        '--save',
        action='store_true',
        help="Save video to file"
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help="Output path for video"
    )
    
    parser.add_argument(
        '--test-connection',
        action='store_true',
        help="Test connection only"
    )
    
    args = parser.parse_args()
    
    if args.test_connection:
        asyncio.run(test_connection())
    else:
        asyncio.run(interactive_demo(
            prompt=args.prompt,
            duration=args.duration,
            portrait=args.portrait,
            save_video=args.save,
            output_path=args.output
        ))


if __name__ == "__main__":
    import logging
    main()
