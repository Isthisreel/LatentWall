# WHAT DI U MEAN - Quick Start

## 🎤 Speech-to-Visual Translator

Convert your speech into AI-generated video in real-time!

---

## Setup (One-Time)

### 1. Download Vosk Model

The speech recognition needs a language model. Download the small English model:

**Windows (PowerShell)**:
```powershell
# Create models directory
mkdir backend\models

# Download Vosk model (~ 40MB)
Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip" -OutFile "backend\models\vosk-model.zip"

# Extract
Expand-Archive -Path "backend\models\vosk-model.zip" -DestinationPath "backend\models\"
```

### 2. Verify Installation

Check that Vosk installed successfully:
```powershell
cd backend
..\.venv\Scripts\python -c "import vosk; print('✅ Vosk installed!')"
```

---

## Running the Test

### Start the Odyssey Backend

If not already running:
```powershell
cd backend
..\.venv\Scripts\python main.py
```

Keep this running in one terminal.

### Run Speech-to-Video Test

In a NEW terminal:
```powershell
cd backend
..\.venv\Scripts\python test_speech_to_video.py
```

### What to Expect

```
🎤 WHAT DI U MEAN - Speech-to-Visual Translator
============================================================

Speak clearly into your microphone!
Try saying:
  - 'cat'
  - 'red car'
  - 'big blue dragon'

Press Ctrl+C to stop

🎤 Starting microphone...
✅ Listening... Speak now!
```

### Try These Phrases

| Say This | You'll See |
|----------|------------|
| "cat" | A fluffy domestic cat |
| "red car" | A vibrant crimson red sleek modern car |
| "big dragon" | An enormous and towering majestic mythical dragon |
| "scary dark forest" | A frightening and terrifying shadowy and ominous dense green forest |

---

## How It Works

```
Your Voice
    ↓
[Vosk STT] → "red car"
    ↓
[Keyword Extractor] → ["red", "car"]
    ↓
[Prompt Builder] → "vibrant crimson red, sleek modern car"
    ↓
[Odyssey API] → Generates video (40ms)
    ↓
Video ready! (check playground.html)
```

---

## Checking Generated Videos

After speaking, you'll see:
```
✅ Video generation started! Job ID: abc123...
📺 Check status at: http://localhost:8000/job/abc123...
🌐 Or open playground: http://localhost:5173/playground.html
```

Open the playground URL and paste the job ID to see your video!

---

## Troubleshooting

### "Microphone not detected"
- Check Windows microphone permissions
- Ensure mic is set as default input device

### "Vosk model not found"
- Make sure you downloaded and extracted the model
- Path should be: `backend/models/vosk-model-small-en-us-0.15/`

### "No speech detected"
- Speak louder
- Reduce background noise
- Check mic input levels in Windows settings

### "Word not recognized"
Only 37 words are supported in Phase 1:
- **Nouns**: cat, dog, car, dragon, ocean, forest, city, dinosaur, robot, castle, mountain, bird, tree, flower, house
- **Adjectives**: red, blue, green, yellow, dark, bright, fast, slow, big, small, happy, sad, scary, beautiful
- **Verbs**: running, flying, swimming, jumping, dancing, exploding, glowing, burning

---

## Next Steps

**Phase 2**: Real-time streaming (continuous video morphing)
**Phase 3**: Expand to 200+ words
**Phase 4**: AI interpretation (understand metaphors!)

---

## Current Limitations

- ⏱️ Latency: ~5-10 seconds (batch generation)
- 📝 Vocabulary: Only 37 words
- 🎯 Accuracy: Direct translation only (no metaphors)

**Coming Soon**: Sub-500ms latency with interactive streaming!
