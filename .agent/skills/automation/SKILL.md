---
name: Script Runner & Automation
description: Execute Python scripts and automate tasks directly within the environment
---

# Script Runner & Automation Skill

## Purpose

This skill enables **direct script execution** and automation tasks within the development environment, allowing rapid prototyping, testing, and task automation without manual intervention.

## Triggers

- User requests script execution
- Need to run tests or validation
- Batch operations required
- User says "run", "execute", "automate"
- Data processing tasks
- File operations needed

## Execution Checklist

### Phase 1: Script Assessment
- [ ] **Understand Goal**: What does the script need to do?
- [ ] **Identify Inputs**: What data/files are needed?
- [ ] **Check Dependencies**: Are required packages installed?
- [ ] **Verify Safety**: No destructive operations without confirmation

### Phase 2: Script Creation
- [ ] **Write Clear Code**: Well-commented, readable
- [ ] **Add Error Handling**: Try/except blocks for failures
- [ ] **Add Logging**: Progress indicators for long operations
- [ ] **Validate Inputs**: Check file existence, format, etc.
- [ ] **Set Auto-run Flag**: SafeToAutoRun based on risk

### Phase 3: Execution
- [ ] **Set Working Directory**: Cwd parameter
- [ ] **Configure Timeout**: WaitMsBeforeAsync parameter
- [ ] **Run Command**: Execute via run_command tool
- [ ] **Monitor Output**: Check command_status if background

### Phase 4: Validation
- [ ] **Check Exit Code**: 0 = success, non-zero = error
- [ ] **Review Output**: Verify expected results
- [ ] **Handle Errors**: Debug if failed
- [ ] **Document Results**: Note what was accomplished

## Patterns & Examples

### Pattern 1: Safe Auto-Run Script

```python
# Export project code to single file
# This is safe - only reads files, doesn't modify

await run_command(
    CommandLine="python export_project.py",
    Cwd="C:\\Users\\isma_\\Desktop\\NEW PROJECT",
    SafeToAutoRun=True,  # Safe: only reads/writes output file
    WaitMsBeforeAsync=3000
)
```

### Pattern 2: Unsafe Script (Requires Approval)

```python
# Delete old output files
# This is unsafe - deletes data

await run_command(
    CommandLine="python cleanup_outputs.py --delete-all",
    Cwd="C:\\Users\\isma_\\Desktop\\NEW PROJECT",
    SafeToAutoRun=False,  # Unsafe: deletes files
    WaitMsBeforeAsync=1000
)
# User must approve before execution
```

### Pattern 3: Background Task with Status Checking

```python
# Long-running batch video generation
command_id = await run_command(
    CommandLine="python examples/batch_generator.py --batch ./scripts",
    Cwd="C:\\Users\\isma_\\Desktop\\NEW PROJECT",
    SafeToAutoRun=False,
    WaitMsBeforeAsync=500  # Send to background quickly
)

# Check status periodically
status = await command_status(
    CommandId=command_id,
    WaitDurationSeconds=30,
    OutputCharacterCount=2000
)
```

### Pattern 4: Data Processing Script

```python
"""
Process CSV data and generate visualizations.
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def process_data(input_file: str, output_dir: str):
    # Validate inputs
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load and process
    df = pd.read_csv(input_path)
    
    # Generate visualization
    plt.figure(figsize=(10, 6))
    df.plot(kind='bar')
    plt.savefig(output_path / 'chart.png')
    
    print(f"✅ Processed {len(df)} rows")
    print(f"✅ Saved to {output_path}/chart.png")

if __name__ == "__main__":
    process_data('data.csv', 'outputs')
```

### Pattern 5: Test Runner Automation

```python
# Run all tests
await run_command(
    CommandLine="pytest tests/ -v",
    Cwd="C:\\Users\\isma_\\Desktop\\NEW PROJECT",
    SafeToAutoRun=True,  # Safe: only runs tests
    WaitMsBeforeAsync=10000  # Wait for tests to complete
)

# Run with coverage
await run_command(
    CommandLine="pytest --cov=src --cov-report=html",
    Cwd="C:\\Users\\isma_\\Desktop\\NEW PROJECT",
    SafeToAutoRun=True,
    WaitMsBeforeAsync=15000
)
```

## Common Automation Tasks

### Task 1: Export Project Context

```python
"""Export all code to single file for sharing."""
# Created in export_project.py
# Auto-run: Yes (only reads files)
```

### Task 2: Batch Video Generation

```python
"""Generate multiple videos from script files."""
# Script: examples/batch_generator.py
# Auto-run: No (API calls, potential cost)
```

### Task 3: Update Dependencies

```python
"""Update requirements.txt with latest versions."""
await run_command(
    CommandLine="pip freeze > requirements.txt",
    Cwd="C:\\Users\\isma_\\Desktop\\NEW PROJECT",
    SafeToAutoRun=True,
    WaitMsBeforeAsync=3000
)
```

### Task 4: Code Quality Checks

```python
"""Run linters and formatters."""
# Black formatter
await run_command(
    CommandLine="black src/ examples/ --line-length 100",
    Cwd="C:\\Users\\isma_\\Desktop\\NEW PROJECT",
    SafeToAutoRun=True,
    WaitMsBeforeAsync=5000
)

# Flake8 linter
await run_command(
    CommandLine="flake8 src/ --max-line-length=100",
    Cwd="C:\\Users\\isma_\\Desktop\\NEW PROJECT",
    SafeToAutoRun=True,
    WaitMsBeforeAsync=3000
)
```

### Task 5: Documentation Generation

```python
"""Generate API documentation."""
await run_command(
    CommandLine="pdoc --html --output-dir docs src/",
    Cwd="C:\\Users\\isma_\\Desktop\\NEW PROJECT",
    SafeToAutoRun=True,
    WaitMsBeforeAsync=5000
)
```

## Safety Guidelines

### ✅ Safe to Auto-Run
- Reading files
- Running tests
- Code formatting/linting
- Generating documentation
- Exporting data
- Installing dependencies (via requirements.txt)

### ❌ Requires User Approval
- Deleting files
- Modifying database
- Making API calls (potential cost)
- System configuration changes
- Network requests
- File uploads/downloads
```

## Anti-Patterns

❌ **DON'T** auto-run destructive operations
```python
# BAD
await run_command(
    CommandLine="rm -rf outputs/",  # Deletes everything!
    SafeToAutoRun=True  # WRONG!
)
```

✅ **DO** require approval for destructive ops
```python
# GOOD
await run_command(
    CommandLine="python cleanup.py --confirm",
    SafeToAutoRun=False  # User must approve
)
```

❌ **DON'T** ignore errors
```python
# BAD
result = await run_command(...)
# Didn't check exit code or output
```

✅ **DO** check results
```python
# GOOD
result = await run_command(...)
if result.exit_code != 0:
    logger.error("Command failed", output=result.output)
    raise RuntimeError("Automation failed")
```

❌ **DON'T** hardcode paths
```python
# BAD
CommandLine="python C:\\Users\\isma_\\script.py"
```

✅ **DO** use relative paths or variables
```python
# GOOD
project_dir = "C:\\Users\\isma_\\Desktop\\NEW PROJECT"
CommandLine="python scripts/process.py"
Cwd=project_dir
```

## Integration

### With Planning Skill
- Include automation tasks in implementation plans
- Design scripts for repeatability
- Plan batch operations

### With Troubleshooting Skill
- Run diagnostics scripts to identify issues
- Automate log collection
- Test error scenarios

### With NotebookLM Skill
- Automate research data extraction
- Batch process notebook sources
- Generate reports from research

### With Odyssey ML
- Automate video generation workflows
- Batch process simulation scripts
- Collect and organize recordings

## Script Templates

### Template 1: Basic Task Script

```python
"""
Task: [Description]
Author: [Name]
Date: [Date]
"""

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting task...")
        
        # Your logic here
        result = do_work()
        
        logger.info(f"✅ Task complete: {result}")
        return 0
        
    except Exception as e:
        logger.error(f"❌ Task failed: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit(main())
```

### Template 2: CLI Script with Arguments

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Task description")
    parser.add_argument('--input', required=True, help="Input file")
    parser.add_argument('--output', default='output', help="Output directory")
    parser.add_argument('--verbose', action='store_true', help="Verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    # Process
    process(args.input, args.output)

if __name__ == "__main__":
    main()
```

## Automation Best Practices

1. **Idempotent**: Script can run multiple times safely
2. **Validated**: Check inputs before processing
3. **Logged**: Progress indicators for visibility
4. **Atomic**: All-or-nothing operations when possible
5. **Recoverable**: Can resume from failure point
6. **Documented**: Clear comments and usage instructions
7. **Tested**: Run with sample data before production

---

**Remember**: "Automate repetitive tasks, but always verify safety first."
