"""
Simulation Manager

Orchestrates batch video generation using Odyssey's Simulate API.
Handles job queue management, status polling, and result collection.
"""

import asyncio
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import json
import aiohttp
import aiofiles
import structlog

from odyssey import Odyssey

logger = structlog.get_logger()


@dataclass
class SimulationScript:
    """
    Represents a simulation script with typed actions.
    
    Example:
        >>> script = SimulationScript()
        >>> script.add_start("A robot dancing", timestamp_ms=0)
        >>> script.add_interact("Robot breakdances", timestamp_ms=5000)
        >>> script.add_end(timestamp_ms=10000)
    """
    
    def __init__(self):
        self.actions: List[Dict[str, Any]] = []
    
    def add_start(
        self,
        prompt: str,
        timestamp_ms: int = 0,
        image: Optional[str | bytes] = None
    ) -> 'SimulationScript':
        """
        Add start action.
        
        Args:
            prompt: Initial text prompt
            timestamp_ms: When to start (usually 0)
            image: Optional image for image-to-video
            
        Returns:
            Self for chaining
        """
        action = {
            "timestamp_ms": timestamp_ms,
            "start": {
                "prompt": prompt
            }
        }
        
        if image is not None:
            action["start"]["image"] = image
        
        self.actions.append(action)
        return self
    
    def add_interact(
        self,
        prompt: str,
        timestamp_ms: int
    ) -> 'SimulationScript':
        """
        Add interaction action.
        
        Args:
            prompt: Interaction prompt
            timestamp_ms: When to interact (milliseconds)
            
        Returns:
            Self for chaining
        """
        self.actions.append({
            "timestamp_ms": timestamp_ms,
            "interact": {
                "prompt": prompt
            }
        })
        return self
    
    def add_end(self, timestamp_ms: int) -> 'SimulationScript':
        """
        Add end action.
        
        Args:
            timestamp_ms: When to end stream
            
        Returns:
            Self for chaining
        """
        self.actions.append({
            "timestamp_ms": timestamp_ms,
            "end": {}
        })
        return self
    
    def to_dict(self) -> List[Dict[str, Any]]:
        """Convert to dict format for Odyssey API."""
        return self.actions
    
    @classmethod
    def from_file(cls, filepath: str | Path) -> 'SimulationScript':
        """
        Load script from JSON file.
        
        Args:
            filepath: Path to JSON script file
            
        Returns:
            SimulationScript instance
        """
        with open(filepath, 'r') as f:
            actions = json.load(f)
        
        script = cls()
        script.actions = actions
        return script
    
    async def to_file(self, filepath: str | Path) -> None:
        """
        Save script to JSON file.
        
        Args:
            filepath: Output path
        """
        async with aiofiles.open(filepath, 'w') as f:
            await f.write(json.dumps(self.actions, indent=2))
        
        logger.info("Script saved", filepath=str(filepath))


class SimulationManager:
    """
    Manages batch simulation jobs.
    
    Example:
        >>> manager = SimulationManager()
        >>> script = SimulationScript()
        >>> script.add_start("A cat", 0).add_end(10000)
        >>> job_id = await manager.submit(script)
        >>> result = await manager.wait_for_completion(job_id)
        >>> await manager.download_result(result)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: Odyssey API key (uses env var if not provided)
        """
        self.client = Odyssey(api_key=api_key) if api_key else Odyssey()
        self.active_jobs: Dict[str, Dict] = {}
        logger.info("SimulationManager initialized")
    
    async def submit(
        self,
        script: SimulationScript | List[Dict],
        portrait: bool = True,
        job_name: Optional[str] = None
    ) -> str:
        """
        Submit a simulation job.
        
        Args:
            script: SimulationScript or raw dict list
            portrait: Video orientation
            job_name: Optional name for tracking
            
        Returns:
            job_id: Unique job identifier
        """
        if isinstance(script, SimulationScript):
            script_data = script.to_dict()
        else:
            script_data = script
        
        logger.info(
            "Submitting simulation",
            action_count=len(script_data),
            portrait=portrait,
            name=job_name
        )
        
        job = await self.client.simulate(
            script=script_data,
            portrait=portrait
        )
        
        self.active_jobs[job.job_id] = {
            'job_id': job.job_id,
            'name': job_name or job.job_id,
            'status': job.status,
            'submitted_at': asyncio.get_event_loop().time()
        }
        
        logger.info("Job submitted", job_id=job.job_id, name=job_name)
        return job.job_id
    
    async def get_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get current status of a job.
        
        Args:
            job_id: Job identifier
            
        Returns:
            Status dict with job details
        """
        status = await self.client.get_simulate_status(job_id)
        
        status_dict = {
            'job_id': status.job_id,
            'status': status.status,
            'streams': [
                {'stream_id': s.stream_id}
                for s in (status.streams or [])
            ],
            'error': status.error_message if hasattr(status, 'error_message') else None
        }
        
        # Update active jobs
        if job_id in self.active_jobs:
            self.active_jobs[job_id]['status'] = status.status
        
        logger.info(
            "Status retrieved",
            job_id=job_id,
            status=status.status
        )
        
        return status_dict
    
    async def wait_for_completion(
        self,
        job_id: str,
        poll_interval: int = 5,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Wait for job to complete.
        
        Args:
            job_id: Job identifier
            poll_interval: Seconds between status checks
            timeout: Max seconds to wait (None = unlimited)
            
        Returns:
            Final status dict
            
        Raises:
            TimeoutError: If timeout exceeded
            RuntimeError: If job failed
        """
        logger.info(
            "Waiting for completion",
            job_id=job_id,
            poll_interval=poll_interval
        )
        
        start_time = asyncio.get_event_loop().time()
        
        while True:
            status = await self.get_status(job_id)
            
            # Check if done
            if status['status'] not in ('pending', 'running'):
                break
            
            # Check timeout
            if timeout:
                elapsed = asyncio.get_event_loop().time() - start_time
                if elapsed > timeout:
                    raise TimeoutError(
                        f"Job {job_id} timed out after {elapsed:.1f}s"
                    )
            
            await asyncio.sleep(poll_interval)
        
        # Check if failed
        if status['status'] == 'failed':
            error_msg = status.get('error', 'Unknown error')
            logger.error("Job failed", job_id=job_id, error=error_msg)
            raise RuntimeError(f"Job failed: {error_msg}")
        
        if status['status'] == 'cancelled':
            logger.warning("Job was cancelled", job_id=job_id)
            raise RuntimeError("Job was cancelled")
        
        logger.info("Job completed", job_id=job_id)
        return status
    
    async def cancel(self, job_id: str) -> None:
        """
        Cancel a pending or running job.
        
        Args:
            job_id: Job to cancel
        """
        logger.info("Cancelling job", job_id=job_id)
        
        await self.client.cancel_simulation(job_id)
        
        if job_id in self.active_jobs:
            self.active_jobs[job_id]['status'] = 'cancelled'
        
        logger.info("Job cancelled", job_id=job_id)
    
    async def download_result(
        self,
        status: Dict[str, Any],
        output_dir: str | Path = "./outputs"
    ) -> List[Path]:
        """
        Download all videos from completed job.
        
        Args:
            status: Status dict from wait_for_completion
            output_dir: Directory for downloads
            
        Returns:
            List of downloaded file paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        job_id = status['job_id']
        streams = status.get('streams', [])
        
        if not streams:
            logger.warning("No streams in result", job_id=job_id)
            return []
        
        logger.info(
            "Downloading results",
            job_id=job_id,
            stream_count=len(streams)
        )
        
        downloaded = []
        
        for i, stream in enumerate(streams):
            stream_id = stream['stream_id']
            recording = await self.client.get_recording(stream_id)
            
            # Download video
            video_path = output_dir / f"{job_id}_stream_{i}.mp4"
            await self._download_file(recording.video_url, video_path)
            downloaded.append(video_path)
            
            # Download thumbnail
            thumb_path = output_dir / f"{job_id}_stream_{i}_thumb.jpg"
            await self._download_file(recording.thumbnail_url, thumb_path)
            downloaded.append(thumb_path)
            
            logger.info(
                "Stream downloaded",
                stream_id=stream_id,
                video=str(video_path)
            )
        
        logger.info("All downloads complete", count=len(downloaded))
        return downloaded
    
    async def _download_file(self, url: str, output_path: Path) -> None:
        """Download file from URL."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                
                async with aiofiles.open(output_path, 'wb') as f:
                    await f.write(await resp.read())
    
    def list_active_jobs(self) -> List[Dict]:
        """Get list of tracked active jobs."""
        return list(self.active_jobs.values())


class BatchProcessor:
    """
    Process multiple simulations in parallel.
    
    Example:
        >>> processor = BatchProcessor(max_concurrent=3)
        >>> 
        >>> scripts = [
        ...     SimulationScript().add_start("Cat", 0).add_end(5000),
        ...     SimulationScript().add_start("Dog", 0).add_end(5000),
        ... ]
        >>> 
        >>> results = await processor.process_batch(scripts)
    """
    
    def __init__(
        self,
        max_concurrent: int = 5,
        api_key: Optional[str] = None
    ):
        """
        Args:
            max_concurrent: Max simultaneous jobs
            api_key: Odyssey API key
        """
        self.max_concurrent = max_concurrent
        self.manager = SimulationManager(api_key=api_key)
        self.semaphore = asyncio.Semaphore(max_concurrent)
        logger.info(
            "BatchProcessor initialized",
            max_concurrent=max_concurrent
        )
    
    async def process_batch(
        self,
        scripts: List[SimulationScript | List[Dict]],
        output_dir: str | Path = "./outputs",
        portrait: bool = True
    ) -> List[Dict]:
        """
        Process multiple scripts in parallel.
        
        Args:
            scripts: List of simulation scripts
            output_dir: Output directory
            portrait: Video orientation
            
        Returns:
            List of result dicts
        """
        logger.info("Starting batch processing", count=len(scripts))
        
        tasks = [
            self._process_single(script, i, output_dir, portrait)
            for i, script in enumerate(scripts)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Count successes/failures
        successes = sum(
            1 for r in results
            if not isinstance(r, Exception)
        )
        
        logger.info(
            "Batch complete",
            total=len(scripts),
            successes=successes,
            failures=len(scripts) - successes
        )
        
        return results
    
    async def _process_single(
        self,
        script: SimulationScript | List[Dict],
        index: int,
        output_dir: Path,
        portrait: bool
    ) -> Dict:
        """Process single script with semaphore control."""
        async with self.semaphore:
            try:
                job_id = await self.manager.submit(
                    script,
                    portrait=portrait,
                    job_name=f"batch_{index}"
                )
                
                status = await self.manager.wait_for_completion(job_id)
                
                paths = await self.manager.download_result(
                    status,
                    output_dir=output_dir
                )
                
                return {
                    'index': index,
                    'job_id': job_id,
                    'status': 'success',
                    'files': [str(p) for p in paths]
                }
                
            except Exception as e:
                logger.error(
                    "Batch item failed",
                    index=index,
                    error=str(e)
                )
                return {
                    'index': index,
                    'status': 'failed',
                    'error': str(e)
                }
