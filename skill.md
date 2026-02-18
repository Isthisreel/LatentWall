# Skill: Odyssey Visual Director

## Trigger
Use this skill whenever I ask to "generate visuals," "visualize audio," or "connect to Odyssey."

## Workflow
1. **API Validation:**
   - Before writing code, query the connected NotebookLM for "Odyssey API Authentication" and "Endpoint Structure" to ensure we use the latest methods.

2. **Lore Injection:**
   - When constructing the visual prompt for Odyssey, ALWAYS query NotebookLM for the "Dino 26 Lore Bible."
   - Extract keywords about color palette, atmosphere, and "Dino" character design.

3. **Audio-Reactive Logic:**
   - If I provide audio characteristics (e.g., "120 BPM, Aggressive"), use the "Audio-Visual Mapping" document in NotebookLM to decide camera movement and lighting.

4. **Code Generation:**
   - Write a Python function `generate_odyssey_scene(audio_features)` that constructs the API request.
   - Include error handling for GCloud timeouts (set timeout to 300s).

## Critical Rule
Never guess the Odyssey API parameters. Always verify them against the NotebookLM documentation first.