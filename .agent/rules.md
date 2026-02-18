# Odyssey ML Project - Development Rules

## Python Environment

1. **Python Version**: All code MUST use Python 3.12 or higher
2. **Type Hints**: Use type hints for all function signatures
3. **Async/Await**: All Odyssey operations MUST use async/await patterns

## Odyssey SDK Standards

### Resource Management

1. **Always use try/finally blocks** for client connections:
```python
client = Odyssey(api_key="...")
try:
    await client.connect(...)
    # ... operations ...
finally:
    await client.disconnect()  # MANDATORY cleanup
```

2. **Never forget disconnect()** - Resource leaks are critical failures

### Error Handling

1. **Catch specific exceptions**:
   - `OdysseyAuthError` - Authentication failures
   - `OdysseyConnectionError` - Connection issues
   - `OdysseyStreamError` - Stream operation errors

2. **Handle fatal vs recoverable errors**:
```python
def on_error(error: Exception, fatal: bool):
    if fatal:
        # Must reconnect or exit
        logger.error(f"Fatal error: {error}")
    else:
        # Can continue
        logger.warning(f"Recoverable error: {error}")
```

### API Selection

1. **Interactive API** (`start_stream`, `interact`, `end_stream`):
   - Use for real-time user interaction
   - Use when immediate feedback is needed
   - Use for live streaming scenarios

2. **Simulate API** (`simulate`, `get_simulate_status`):
   - Use for batch processing
   - Use for pre-scripted sequences
   - Use for background tasks
   - Use when user doesn't need real-time updates

### Frame Processing

1. **Always copy frame data** if storing:
```python
def on_video_frame(frame: VideoFrame):
    frames.append(frame.data.copy())  # copy() is mandatory
```

2. **Process frames asynchronously** to avoid blocking the event loop

### Image-to-Video

1. **Validate image constraints** before processing:
   - Max size: 25 MB
   - Supported formats: JPEG, PNG, WebP, GIF, BMP, HEIC, HEIF, AVIF

2. **Accept multiple image types** in functions:
```python
def process_image(image: str | bytes | Image.Image | np.ndarray):
    # Handle all supported types
    pass
```

## Code Organization

### File Structure

```
src/
├── odyssey_client.py      # Client wrapper and management
├── video_processor.py     # Frame processing utilities
└── simulation_manager.py  # Batch job orchestration

examples/
├── interactive_demo.py    # Real-time streaming demo
├── batch_generator.py     # Batch processing demo
├── image_to_video.py      # Image-to-video demo
└── headless_demo.py       # ML workflow demo
```

### Module Responsibilities

1. **odyssey_client.py**: Singleton pattern, connection management, logging
2. **video_processor.py**: Frame format conversion, video file I/O
3. **simulation_manager.py**: Job queue, status polling, result collection

## Environment Variables

1. **Required**:
   - `ODYSSEY_API_KEY` - Odyssey API key (starts with `ody_`)

2. **Optional**:
   - `ODYSSEY_LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
   - `ODYSSEY_OUTPUT_DIR` - Default output directory for videos

## Documentation

### Code Comments

1. **Document all async functions** with docstrings including:
   - Purpose
   - Parameters with types
   - Return values
   - Exceptions raised
   - Example usage

### Example Docstring

```python
async def generate_video(
    prompt: str,
    image: str | None = None,
    portrait: bool = True
) -> str:
    """
    Generate a video using Odyssey ML.
    
    Args:
        prompt: Text description for video generation
        image: Optional image path for image-to-video
        portrait: If True, generate 704x1280, else 1280x704
        
    Returns:
        stream_id: Unique identifier for the generated stream
        
    Raises:
        OdysseyAuthError: If API key is invalid
        OdysseyConnectionError: If connection fails
        
    Example:
        >>> stream_id = await generate_video("A cat playing", portrait=True)
        >>> recording = await client.get_recording(stream_id)
    """
```

## Testing

1. **Test authentication** before running production code
2. **Use simulate API** for testing to avoid real-time resource usage
3. **Mock external dependencies** in unit tests
4. **Test error scenarios**: no streamers, timeout, auth failure

## Performance

1. **Reuse client instances** - Don't create new clients repeatedly
2. **Use simulate API** for batch operations - More efficient than multiple interactive streams
3. **Download recordings immediately** - URLs expire after 1 hour
4. **Process frames asynchronously** - Don't block the event loop
5. **Set reasonable polling intervals** - Minimum 5s for simulate status checks

## Security

1. **Never commit API keys** to version control
2. **Use environment variables** for all secrets
3. **Validate all user input** before passing to Odyssey API
4. **Sanitize file paths** before processing images

## Logging

1. **Use structured logging**:
```python
logger.info("Stream started", extra={
    "stream_id": stream_id,
    "prompt": prompt,
    "portrait": portrait
})
```

2. **Log levels**:
   - DEBUG: Frame processing details
   - INFO: Stream lifecycle events
   - WARNING: Recoverable errors
   - ERROR: Fatal errors, authentication failures

## NotebookLM Integration

1. **Query NotebookLM** for implementation guidance before writing new Odyssey code
2. **Use notebook ID**: `f1b09888-005d-444f-8a4f-0db1a2fc1929`
3. **Verify features** against documentation before implementing

## Version Control

1. **Commit message format**: `[component] brief description`
   - Examples: `[client] Add reconnection logic`, `[docs] Update SDK examples`

2. **Ignore files** (.gitignore):
   ```
   .env
   outputs/
   __pycache__/
   *.pyc
   .venv/
   ```

## Common Pitfalls to Avoid

❌ **DON'T**:
- Use Python < 3.12
- Forget `disconnect()` in finally blocks
- Try to interact when disconnected
- Use interactive API for batch tasks
- Store frame data without `.copy()`
- Ignore fatal errors from error callbacks
- Upload images > 25 MB
- Expect recording URLs to last forever (1-hour max)

✅ **DO**:
- Always use try/finally
- Choose correct API (interactive vs simulate)
- Handle all error types explicitly
- Validate constraints before API calls
- Log all significant events
- Test edge cases (no streamers, timeouts)
