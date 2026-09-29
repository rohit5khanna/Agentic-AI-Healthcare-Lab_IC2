# Agentic AI Healthcare Lab

An interactive learning repository for understanding how healthcare AI agents reason, use tools, interact with structured environments, expose uncertainty, and remain subject to technical and human controls.

The repository provides the same ten-part curriculum in two complementary formats:

- **[Agentic Demos Jupyter](<Agentic Demos Jupyter/>)** — ten detailed notebooks for sequential study, code inspection, exercises, and experimentation.
- **[Agentic Learning Lab Marimo](<Agentic Learning Lab Marimo/>)** — one participant-facing interactive application with a Home page and menu for all ten demonstrations.

All cases and records are fictional or synthetic. This repository is intended for research and education; it is not a clinical protocol or patient-care system.

## Curriculum

| # | Demonstration | Central question |
|---:|---|---|
| 1 | LLM versus deterministic tool | Which work belongs to language generation, tools, or people? |
| 2 | Minimal agent loop | What makes an agent different from a single model response? |
| 3 | Human approval gate | How can consequential actions be stopped by architecture? |
| 4 | Memory and stale facts | What happens when remembered information is no longer current? |
| 5 | Tool retrieval and routing | Which tools and models should be available for a task? |
| 6 | Uncertainty and abstention | When should the system stop and escalate? |
| 7 | Compounding reliability | Why can reliable-looking steps produce an unreliable workflow? |
| 8 | Orchestrators and specialists | When does a multi-agent design justify its complexity? |
| 9 | FHIR sandbox | How do synthetic patient records become an agent environment? |
| 10 | Prompt injection | Why must safety controls live outside the prompt? |

## Choose an interface

### Jupyter

Use Jupyter when you want to work through the curriculum step by step, inspect every code cell, and modify the implementation.

```bash
cd "Agentic Demos Jupyter"
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
export LAB_MODE=mock
jupyter lab
```

### Marimo

Use Marimo for a workshop-friendly, single-application experience that lets participants select any demonstration from a curriculum menu.

```bash
cd "Agentic Learning Lab Marimo"
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
marimo run healthcare_agent_learning_lab.py
```

## Execution modes

- **Explore:** deterministic teaching behavior with no API key.
- **Replay:** preserved representative behavior with no new model call.
- **Live:** authentic model behavior with visible latency and token use. Live mode requires `OPENAI_API_KEY` and `MODEL` in the environment.

Never place an API key in a notebook cell or commit it to the repository. Copy `.env.example` to an untracked `.env`, or configure credentials in the shell that launches the application.

## Interpretation boundary

Successful execution demonstrates software behavior, tool boundaries, and workshop concepts. It does not establish clinical correctness, comparative model superiority, or readiness for use with real patients.
