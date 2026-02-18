---
description: Initial Odyssey ML project setup
---

# Setup Odyssey ML Project

This workflow sets up the complete Odyssey ML development environment.

## Steps

### 1. Verify Python Version
// turbo
```bash
python --version
```
**Expected**: Python 3.12.0 or higher

### 2. Install Odyssey SDK
// turbo
```bash
pip install git+https://github.com/odysseyml/odyssey-python.git
```

### 3. Verify SDK Installation
// turbo
```bash
python -c "import odyssey; print('Odyssey SDK installed successfully')"
```

### 4. Set Up Environment Variables

Create or update `.env` file with your Odyssey API key:
```
ODYSSEY_API_KEY=ody_your_api_key_here
```

⚠️ **IMPORTANT**: Get your API key from https://odyssey.ml/

### 5. Test API Authentication
// turbo
```bash
python -c "import os; from odyssey import Odyssey; client = Odyssey(api_key=os.getenv('ODYSSEY_API_KEY')); print('Authentication successful')"
```

### 6. Install Optional Dependencies

For OpenCV integration (video display):
```bash
pip install opencv-python
```

For image processing:
```bash
pip install Pillow numpy
```

### 7. Run Connection Test

```bash
python examples/connection_test.py
```

## Verification

✅ Python 3.12+ installed
✅ Odyssey SDK installed
✅ API key configured
✅ Authentication successful
✅ Optional dependencies installed (if needed)

## Troubleshooting

**"No module named 'odyssey'"**
- Re-run: `pip install git+https://github.com/odysseyml/odyssey-python.git`

**"OdysseyAuthError"**
- Check API key in `.env` file
- Verify key starts with `ody_`
- Ensure key is valid at https://odyssey.ml/

**"Python 3.12 required"**
- Install Python 3.12 or higher
- Update your PATH to use the correct Python version
