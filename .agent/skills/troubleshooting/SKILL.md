---
name: Troubleshooting & Error Handling
description: Systematic approach to debugging with error handling patterns and logging best practices
---

# Troubleshooting & Error Handling Skill

## Purpose

This skill provides a **systematic debugging methodology** and error handling patterns to fix bugs efficiently and prevent them from recurring.

## Triggers

- Code throws an error or exception
- User reports a bug
- User says "fix", "error", "broken", "not working"
- Tests are failing
- Unexpected behavior observed
- Performance issues detected

## Execution Checklist

### Phase 1: Error Identification
- [ ] **Capture Error Message**: Full stack trace, error code
- [ ] **Identify Location**: File, line number, function
- [ ] **Note Context**: What user was doing when error occurred
- [ ] **Reproduce**: Can you make it happen consistently?

### Phase 2: Root Cause Analysis
- [ ] **Read the Error**: What does the message actually say?
- [ ] **Check Recent Changes**: What code was modified recently?
- [ ] **Verify Inputs**: Are function arguments what we expect?
- [ ] **Check State**: Are variables/objects in expected states?
- [ ] **Review Logs**: What do application logs show?

### Phase 3: Hypothesis Formation
- [ ] **List Possible Causes**: Brainstorm 3-5 theories
- [ ] **Rank by Likelihood**: Most probable first
- [ ] **Identify Tests**: How to validate each hypothesis

### Phase 4: Solution Implementation
- [ ] **Apply Fix**: Implement most likely solution
- [ ] **Add Error Handling**: Wrap in try/catch if needed
- [ ] **Add Logging**: Log relevant information
- [ ] **Add Validation**: Check inputs/outputs
- [ ] **Test Fix**: Verify error is resolved

### Phase 5: Prevention
- [ ] **Add Unit Test**: Prevent regression
- [ ] **Update Documentation**: Note the issue and fix
- [ ] **Review Similar Code**: Are there other instances?
- [ ] **Improve Error Messages**: Make debugging easier next time

## Patterns & Examples

### Pattern 1: Try-Catch-Finally (Python)

```python
import logging

logger = logging.getLogger(__name__)

async def safe_operation():
    """
    Template for safe async operations with proper error handling.
    """
    resource = None
    
    try:
        # Acquire resource
        resource = await acquire_resource()
        
        # Perform operation
        result = await process(resource)
        
        logger.info("Operation successful", extra={'result': result})
        return result
        
    except SpecificError as e:
        # Handle known errors
        logger.error(
            "Specific error occurred",
            extra={'error': str(e)},
            exc_info=True
        )
        raise  # Re-raise after logging
        
    except Exception as e:
        # Handle unexpected errors
        logger.error(
            "Unexpected error",
            extra={'error': str(e)},
            exc_info=True
        )
        raise
        
    finally:
        # Cleanup
        if resource:
            await resource.close()
            logger.debug("Resource cleaned up")
```

### Pattern 2: Custom Exception Classes

```python
class OdysseyError(Exception):
    """Base exception for Odyssey operations."""
    pass

class OdysseyAuthError(OdysseyError):
    """Raised when authentication fails."""
    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)

class OdysseyConnectionError(OdysseyError):
    """Raised when connection fails."""
    def __init__(self, message="Connection failed", retry_after=None):
        self.message = message
        self.retry_after = retry_after
        super().__init__(self.message)

# Usage
try:
    await connect()
except OdysseyAuthError:
    print("Check your API key")
except OdysseyConnectionError as e:
    if e.retry_after:
        print(f"Retry after {e.retry_after}s")
```

### Pattern 3: Structured Logging

```python
import structlog

logger = structlog.get_logger()

async def generate_video(prompt: str, stream_id: str):
    logger.info(
        "Starting generation",
        prompt=prompt,
        stream_id=stream_id
    )
    
    try:
        result = await odyssey.start_stream(prompt)
        
        logger.info(
            "Generation successful",
            stream_id=stream_id,
            duration_ms=result.duration
        )
        
        return result
        
    except Exception as e:
        logger.error(
            "Generation failed",
            stream_id=stream_id,
            error=str(e),
            error_type=type(e).__name__,
            exc_info=True
        )
        raise
```

### Pattern 4: Input Validation

```python
from typing import Optional

def validate_prompt(prompt: str, max_length: int = 1000) -> str:
    """
    Validate and sanitize user prompt.
    
    Raises:
        ValueError: If prompt is invalid
    """
    if not prompt:
        raise ValueError("Prompt cannot be empty")
    
    if not isinstance(prompt, str):
        raise TypeError(f"Prompt must be string, got {type(prompt)}")
    
    if len(prompt) > max_length:
        raise ValueError(f"Prompt too long ({len(prompt)} > {max_length})")
    
    # Sanitize
    prompt = prompt.strip()
    
    return prompt

# Usage
try:
    clean_prompt = validate_prompt(user_input)
    await generate(clean_prompt)
except ValueError as e:
    logger.warning("Invalid prompt", error=str(e))
    return {"error": str(e)}
```

### Pattern 5: Retry Logic

```python
import asyncio
from typing import Callable, TypeVar

T = TypeVar('T')

async def retry_with_backoff(
    func: Callable[[], T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0
) -> T:
    """
    Retry function with exponential backoff.
    """
    for attempt in range(max_retries):
        try:
            return await func()
            
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error("Max retries exceeded", error=str(e))
                raise
            
            delay = min(base_delay * (2 ** attempt), max_delay)
            logger.warning(
                "Retrying after error",
                attempt=attempt + 1,
                max_retries=max_retries,
                delay=delay,
                error=str(e)
            )
            
            await asyncio.sleep(delay)

# Usage
result = await retry_with_backoff(
    lambda: odyssey_client.connect(),
    max_retries=3
)
```

## Anti-Patterns

❌ **DON'T** use bare except
```python
# BAD
try:
    risky_operation()
except:
    pass  # Silently swallows all errors!
```

✅ **DO** catch specific exceptions
```python
# GOOD
try:
    risky_operation()
except ValueError as e:
    logger.error("Invalid value", error=str(e))
    raise
except KeyError as e:
    logger.error("Missing key", error=str(e))
    raise
```

❌ **DON'T** log without context
```python
# BAD
logger.error("Error occurred")
```

✅ **DO** log with rich context
```python
# GOOD
logger.error(
    "Stream generation failed",
    stream_id=stream_id,
    prompt=prompt,
    error=str(e),
    error_type=type(e).__name__,
    exc_info=True
)
```

❌ **DON'T** ignore error messages
```python
# BAD - Didn't read the error
# Error: "API key must start with 'ody_'"
# Developer: *checks network connection*
```

✅ **DO** read error messages carefully
```python
# GOOD
# Error: "API key must start with 'ody_'"
# Developer: *checks API key format*
```

❌ **DON'T** make assumptions
```python
# BAD
# Assumes user_data is always a dict
name = user_data['name']  # KeyError if missing!
```

✅ **DO** validate assumptions
```python
# GOOD
if not isinstance(user_data, dict):
    raise TypeError("user_data must be dict")

name = user_data.get('name')
if not name:
    raise ValueError("name is required")
```

## Debugging Checklist

When facing a bug:

- [ ] **Read the error message completely**
- [ ] **Check the stack trace** - Where did it fail?
- [ ] **Look at recent changes** - What was modified?
- [ ] **Verify inputs** - Are arguments correct?
- [ ] **Check environment** - API keys, dependencies OK?
- [ ] **Read the docs** - Am I using the API correctly?
- [ ] **Add print/log statements** - What values do variables have?
- [ ] **Simplify** - Can I reproduce with minimal code?
- [ ] **Google the error** - Has someone seen this before?
- [ ] **Ask for help** - Describe the problem clearly

## Common Error Scenarios

### Scenario 1: Import Errors
```python
# Error: ModuleNotFoundError: No module named 'odyssey'

# Checklist:
# - Is the package installed? (pip list)
# - Is the virtual environment activated?
# - Is the package name spelled correctly?
# - Is the Python path configured?
```

### Scenario 2: API Errors
```python
# Error: OdysseyAuthError: Invalid API key

# Checklist:
# - Is API key in .env file?
# - Is .env being loaded? (load_dotenv())
# - Does key start with 'ody_'?
# - Is the key active/valid?
```

### Scenario 3: Async Errors
```python
# Error: RuntimeError: asyncio.run() cannot be called from a running event loop

# Cause: Trying to use asyncio.run() inside async function
# Fix: Use await instead of asyncio.run()

# BAD
async def my_func():
    result = asyncio.run(other_async_func())

# GOOD
async def my_func():
    result = await other_async_func()
```

### Scenario 4: Resource Leaks
```python
# Symptom: "Too many open files" error

# Cause: Not closing resources
# Fix: Use context managers or finally blocks

# BAD
file = open('data.txt')
data = file.read()
# Never closed!

# GOOD
with open('data.txt') as file:
    data = file.read()
# Automatically closed
```

## Integration

### With Planning Skill
- Include error handling in architecture plans
- Design for failure from the start

### With NotebookLM
- Query for error handling best practices
- Search documentation for error codes

### With Odyssey ML
- Handle OdysseyAuthError, OdysseyConnectionError
- Implement retry logic for "no streamers available"
- Log all API interactions

## Error Handling Levels

### Level 1: Basic
```python
try:
    result = operation()
except Exception as e:
    print(f"Error: {e}")
```

### Level 2: Logging
```python
try:
    result = operation()
except Exception as e:
    logger.error("Operation failed", error=str(e), exc_info=True)
    raise
```

### Level 3: Recovery
```python
try:
    result = operation()
except TemporaryError as e:
    logger.warning("Retrying after error", error=str(e))
    await asyncio.sleep(5)
    result = operation()  # Retry once
except PermanentError as e:
    logger.error("Permanent failure", error=str(e))
    return None
```

### Level 4: Production
```python
try:
    result = await operation()
except SpecificError as e:
    logger.error("Known error", error=str(e), exc_info=True)
    metrics.increment('errors.specific')
    await notify_admin(e)
    return fallback_response()
except Exception as e:
    logger.critical("Unexpected error", error=str(e), exc_info=True)
    metrics.increment('errors.unknown')
    await emergency_shutdown()
    raise
finally:
    await cleanup_resources()
```

---

**Remember**: "GoodError handling makes the difference between a tool and a product."
