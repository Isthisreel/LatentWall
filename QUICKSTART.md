# 🦖 Synesthesia Engine - Quick Start Guide (Windows)

## ⚡ Fast Setup (PowerShell Scripts)

I've created automated setup scripts for you!

### Option 1: Automated Setup (Recommended)

**Backend:**
```powershell
.\setup-backend.ps1
```

**Frontend** (in a separate PowerShell window):
```powershell
.\setup-frontend.ps1
```

---

### Option 2: Manual Step-by-Step

#### Backend Setup

```powershell
# 1. Navigate to backend
cd backend

# 2. Install dependencies (using parent venv)
..\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 3. Create .env file
copy .env.template .env
# Edit .env and add: ODYSSEY_API_KEY=ody_your_key_here

# 4. Run server
..\.venv\Scripts\python.exe main.py
```

Backend will start at: **http://localhost:8000**

---

#### Frontend Setup (New PowerShell Window)

```powershell
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Run dev server
npm run dev
```

Frontend will open at: **http://localhost:5173**

---

## 🔑 Important: Odyssey API Key

Before running the backend, you **MUST** add your Odyssey API key:

1. Open `backend\.env`
2. Replace `ody_your_key_here` with your actual key
3. Save the file

**Get a key at**: https://odyssey.ml

---

## 🧪 Testing

1. Open browser: http://localhost:5173
2. Check backend health: http://localhost:8000/health
3. Click **"START LISTENING"** in the UI
4. Make some noise (talk, play music, clap)
5. Watch the visuals generate!

---

## 🐛 Common Issues

### "pip is not recognized"
✅ **Fixed**: I've created scripts that use the full path to your venv's Python.

### "numpy installation is slow"
⏳ **Normal**: numpy builds from source on first install (5-10 minutes). Be patient!

### "Module not found: odyssey"
1. Make sure installation completed successfully
2. Check that all packages in requirements.txt installed
3. Try: `..\.venv\Scripts\python.exe -m pip install git+https://github.com/odysseyml/odyssey-python.git`

### "WebSocket connection failed"
1. Ensure backend is running on port 8000
2. Check for errors in backend terminal
3. Verify .env file has valid API key

### "Microphone access denied"
- Grant permission in browser
- Reload the page
- Use Chrome, Edge, or Firefox (Safari has limited MediaRecorder support)

---

## ✅ Next Steps

Once both servers are running:

1. **Silent**: Barely move → "Dino eye closeup"
2. **Low Energy**: Talk quietly → "Dino on cliff at sunset"
3. **Medium**: Play moderate music → "Dino prowling ruins"
4. **High Energy**: Loud music/yelling → "Dino charging with lightning!"

Enjoy your cyberpunk dinosaur! 🦖✨
