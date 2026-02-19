# LatentWall


## Latent Space Responsiveness in Real-Time World Models
**Title:** Optimization of Asynchronous Interaction in Generative Diffusion Pipelines
**Author:** Isma de Hory
**Date:** January 30, 2026

**LatentWall** is an advanced World Model implementation based on the Odyssey architecture. It leverages a swarm of specialized agents to optimize state-transition learning through a decoupled, desynchronized optimization strategy.

## Project Overview

LatentWall implements a high-fidelity world model that separates the learning of environmental dynamics (state transitions) from policy optimization. By utilizing the **Odyssey ML SDK**, it generates consistent video predictions and simulations, serving as a robust foundation for model-based reinforcement learning agents.

## Optimization: Desynchronization Strategy

Traditional world models often couple state estimation and policy learning, leading to bottlenecks. LatentWall employs **Optimization by Desynchronization**:

1.  **Decoupled Training Loops**: The state-transition model (World Model) and the agent's policy are trained in separate, asynchronous processes.
2.  **Latency Desensitization**: By buffering observations and optimizing on latent trajectories off-policy, the system remains robust to inference latency.
3.  **Asynchronous Rolling Horizon**: Policy planning occurs on a "rolling horizon" of latent states, allowing the agent to plan actions based on future predictions without waiting for immediate sensor feedback.

This approach significantly improves computational efficiency and training stability, allowing for real-time inference even with complex visual inputs.

## Security Architecture

A comprehensive **Zero-Trust Security Audit** has been performed on this repository:

-   **Secret Management**: All API keys (Odyssey, Gemini, OpenAI) are strictly isolated in `.env` files and excluded from version control.
-   **Static Analysis**: Automated scans verify the absence of hardcoded credentials in the codebase.
-   **Swarm-Driven Verification**: A multi-agent swarm protocol ensures that every commit adheres to strict security standards before being pushed.

## Implementation Guide

### Prerequisites

-   Python 3.12+
-   [Odyssey ML API Key](https://odyssey.ml)
-   [Vosk Model](https://alphacephei.com/vosk/models) (for speech input)

### Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/StartUp-Agency/LatentWall.git
    cd LatentWall
    ```

2.  **Environment Setup**:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configuration**:
    Copy the template and add your API keys:
    ```bash
    cp .env.template .env
    # Edit .env and add your ODYSSEY_API_KEY
    ```

4.  **Download Models**:
    Run the setup script to download the required Vosk model:
    ```powershell
    # Windows
    ./scripts/setup-backend.ps1
    ```

### Running the World Model

Start the backend server:
```bash
python backend/main.py
```

Launch the frontend interface:
```bash
cd frontend
npm install
npm run dev
```

## Architecture

-   **Backend**: Python (FastAPI, Odyssey SDK, Vosk)
-   **Frontend**: Vite, TailwindCSS
-   **World Model**: Odyssey ML (Video Generation & Physics Simulation)
