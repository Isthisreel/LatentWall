# Project: Synesthesia Engine (Agentic Visualizer)

## Core Objective
Build an AI agent that listens to audio input and generates consistent, lore-accurate visuals using the Odyssey API. This is the visual engine for the "Dino 26" project.

## Tech Stack
- **Backend:** Python (FastAPI) hosted on Google Cloud Run.
- **AI Vision/Video:** Odyssey API.
- **Knowledge Base:** NotebookLM (via MCP) containing API docs and "Dino 26" lore.
- **Audio Processing:** Librosa (for beat/sentiment detection).

## Architecture
1. **Input:** User uploads audio or streams mic.
2. **Analysis:** Python script extracts BPM, Key, and Energy Level.
3. **Reasoning:** Agent queries NotebookLM: "Given high energy and 'Dino 26' lore, what should the scene look like?"
4. **Action:** Agent constructs a complex JSON payload for the Odyssey API.
5. **Output:** Returns video URL or renders stream.

## Hosting Constraints
- Must be containerized (Docker) for GCloud Run.
- Stateless execution.