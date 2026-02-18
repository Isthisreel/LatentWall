---
description: Generate videos using Odyssey ML
---

# Generate Video with Odyssey ML

This workflow guides you through different video generation methods.

## Interactive Streaming

For real-time, interactive video generation:

### 1. Run Interactive Demo
```bash
python examples/interactive_demo.py --prompt "A serene mountain landscape"
```

### 2. With Custom Parameters
```bash
python examples/interactive_demo.py --prompt "A cat playing" --portrait --duration 10
```

## Image-to-Video

Convert an image to video:

### 1. Prepare Your Image
Ensure image meets requirements:
- Max size: 25 MB
- Format: JPEG, PNG, WebP, GIF, BMP, HEIC, HEIF, or AVIF

### 2. Run Image-to-Video
```bash
python examples/image_to_video.py --image path/to/image.jpg --prompt "The scene comes alive"
```

## Batch Simulation

For pre-scripted, batch video generation:

### 1. Create Script File

Create `script.json`:
```json
[
  {
    "timestamp_ms": 0,
    "start": {
      "prompt": "A robot dancing in a neon city"
    }
  },
  {
    "timestamp_ms": 5000,
    "interact": {
      "prompt": "The robot starts breakdancing"
    }
  },
  {
    "timestamp_ms": 10000,
    "end": {}
  }
]
```

### 2. Run Simulation
```bash
python examples/batch_generator.py --script script.json --portrait
```

### 3. Check Status
```bash
python examples/batch_generator.py --status <job_id>
```

### 4. Download Results
The script automatically downloads videos when complete.
Check the `outputs/` directory.

## Headless Processing

For ML workflows without UI:

```bash
python examples/headless_demo.py --prompt "A busy city" --frames 300
```

## Common Options

- `--prompt`: Text description for video generation
- `--portrait`: Generate portrait video (704x1280), default is landscape
- `--duration`: Duration in seconds (default: 10)
- `--image`: Path to image for image-to-video
- `--output`: Output directory (default: ./outputs)

## Tips

- Use **interactive** for real-time user control
- Use **simulate** for batch processing multiple videos
- Use **headless** for ML/AI processing pipelines
- Recording URLs expire after 1 hour - download immediately
