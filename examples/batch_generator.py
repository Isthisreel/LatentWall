"""
Batch Generator - Process multiple simulations
"""

import asyncio
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from simulation_manager import SimulationManager, SimulationScript, BatchProcessor
import structlog

logger = structlog.get_logger()


async def run_single_simulation(
    script_path: str,
    portrait: bool = True,
    output_dir: str = "./outputs"
):
    """
    Run a single simulation from script file.
    
    Args:
        script_path: Path to JSON script file
        portrait: Video orientation  
        output_dir: Output directory
    """
    manager = SimulationManager()
    
    logger.info("Loading script", path=script_path)
    script = SimulationScript.from_file(script_path)
    
    logger.info("Submitting job")
    job_id = await manager.submit(script, portrait=portrait)
    
    print(f"Job submitted: {job_id}")
    print("Waiting for completion...")
    
    try:
        status = await manager.wait_for_completion(
            job_id,
            poll_interval=5
        )
        
        print(f"✅ Job completed!")
        print(f"Downloading results...")
        
        files = await manager.download_result(status, output_dir)
        
        print(f"\n✅ SUCCESS! Downloaded {len(files)} files:")
        for f in files:
            print(f"  - {f}")
            
    except Exception as e:
        logger.error("Job failed", error=str(e))
        print(f"❌ Job failed: {e}")
        sys.exit(1)


async def check_status(job_id: str):
    """Check status of a job."""
    manager = SimulationManager()
    
    status = await manager.get_status(job_id)
    
    print(f"Job ID: {job_id}")
    print(f"Status: {status['status']}")
    
    if status.get('streams'):
        print(f"Streams: {len(status['streams'])}")
        for i, stream in enumerate(status['streams']):
            print(f"  {i+1}. {stream['stream_id']}")
    
    if status.get('error'):
        print(f"Error: {status['error']}")


async def run_batch(
    scripts_dir: str,
    output_dir: str = "./outputs",
    max_concurrent: int = 3,
    portrait: bool = True
):
    """
    Run multiple simulations in parallel.
    
    Args:
        scripts_dir: Directory containing JSON scripts
        output_dir: Output directory
        max_concurrent: Max parallel jobs
        portrait: Video orientation
    """
    scripts_path = Path(scripts_dir)
    
    if not scripts_path.exists():
        print(f"❌ Directory not found: {scripts_dir}")
        sys.exit(1)
    
    # Load all JSON scripts
    script_files = list(scripts_path.glob("*.json"))
    
    if not script_files:
        print(f"❌ No JSON files found in {scripts_dir}")
        sys.exit(1)
    
    logger.info(f"Found {len(script_files)} scripts")
    
    scripts = [
        SimulationScript.from_file(f)
        for f in script_files
    ]
    
    # Process in batch
    processor = BatchProcessor(max_concurrent=max_concurrent)
    
    print(f"Processing {len(scripts)} scripts...")
    print(f"Max concurrent: {max_concurrent}")
    
    results = await processor.process_batch(
        scripts,
        output_dir=output_dir,
        portrait=portrait
    )
    
    # Summary
    successes = [r for r in results if r.get('status') == 'success']
    failures = [r for r in results if r.get('status') == 'failed']
    
    print(f"\n{'='*50}")
    print(f"BATCH COMPLETE")
    print(f"{'='*50}")
    print(f"✅ Successes: {len(successes)}")
    print(f"❌ Failures: {len(failures)}")
    
    if failures:
        print(f"\nFailed jobs:")
        for f in failures:
            print(f"  - Index {f['index']}: {f.get('error', 'Unknown')}")


async def create_example_script(output_path: str):
    """Create an example simulation script."""
    script = SimulationScript()
    
    script.add_start(
        "A robot dancing in a neon city at night",
        timestamp_ms=0
    ).add_interact(
        "The robot starts breakdancing with incredible moves",
        timestamp_ms=5000
    ).add_interact(
        "Fireworks explode in the background",
        timestamp_ms=8000  
    ).add_end(
        timestamp_ms=12000
    )
    
    await script.to_file(output_path)
    
    print(f"✅ Example script created: {output_path}")
    print(f"\nContent:")
    print(json.dumps(script.to_dict(), indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Odyssey Batch Simulation Generator"
    )
    
    parser.add_argument(
        '--script',
        type=str,
        help="Path to simulation script JSON file"
    )
    
    parser.add_argument(
        '--batch',
        type=str,
        help="Directory containing multiple script files"
    )
    
    parser.add_argument(
        '--status',
        type=str,
        help="Check status of job ID"
    )
    
    parser.add_argument(
        '--create-example',
        type=str,
        help="Create example script at path"
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default="./outputs",
        help="Output directory (default: ./outputs)"
    )
    
    parser.add_argument(
        '--portrait',
        action='store_true',
        help="Generate portrait videos"
    )
    
    parser.add_argument(
        '--max-concurrent',
        type=int,
        default=3,
        help="Max concurrent jobs for batch (default: 3)"
    )
    
    args = parser.parse_args()
    
    if args.create_example:
        asyncio.run(create_example_script(args.create_example))
        
    elif args.status:
        asyncio.run(check_status(args.status))
        
    elif args.script:
        asyncio.run(run_single_simulation(
            args.script,
            portrait=args.portrait,
            output_dir=args.output
        ))
        
    elif args.batch:
        asyncio.run(run_batch(
            args.batch,
            output_dir=args.output,
            max_concurrent=args.max_concurrent,
            portrait=args.portrait
        ))
        
    else:
        parser.print_help()
        print("\nExamples:")
        print("  # Create example script")
        print("  python batch_generator.py --create-example example.json")
        print("\n  # Run single simulation")
        print("  python batch_generator.py --script example.json")
        print("\n  # Run batch")
        print("  python batch_generator.py --batch ./scripts --max-concurrent 5")
        print("\n  # Check job status")
        print("  python batch_generator.py --status JOB_ID")


if __name__ == "__main__":
    main()
