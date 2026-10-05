# Agentic AI Healthcare Lab

An interactive learning repository for understanding how healthcare AI agents reason, use tools, interact with structured environments, expose uncertainty, and remain subject to technical and human controls.

The repository provides the ten-part core curriculum in two complementary formats, plus an Applied Healthcare case exercise in Marimo:

- **[Agentic Demos Jupyter](<Agentic Demos Jupyter/>)** — ten detailed notebooks for sequential study, code inspection, exercises, and experimentation.
- **[Agentic Learning Lab Marimo](<Agentic Learning Lab Marimo/>)** — one participant-facing interactive application with a Barry introduction, ten numbered demos, and a separately labeled Applied Healthcare case.

All cases and records are fictional or synthetic. This repository is intended for research and education; it is not a clinical protocol or patient-care system.

## Open the public learning lab

**[Launch the interactive Marimo learning lab](https://rohit5khanna.github.io/Agentic-AI-Healthcare-Lab_IC2/)**

The public GitHub Pages edition runs entirely in the visitor's browser and provides **Explore** and **Replay** without an API key. Its Applied Healthcare PrEP activity is a learner-directed exercise over summarized synthetic Synthea evidence—not a model response or agent run. Fresh model-directed PrEP runs remain for the authenticated hosted Marimo edition so credentials never enter the public browser application.

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

The Applied Healthcare PrEP case is a separate, unnumbered case study in the Marimo sidebar. It is an interactive learner-directed exercise over summarized synthetic Synthea evidence—not a model response or AI Agent run.

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

Use Marimo locally for the complete interactive learning application, including optional facilitator-controlled Live mode.

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
- **Live:** authentic model behavior with visible latency and token use. Live mode requires `OPENAI_API_KEY` and `MODEL` in a trusted local or server environment and is intentionally disabled on GitHub Pages. The public PrEP activity is an interactive evidence-and-review exercise; it does not make a model call.

Never place an API key in a notebook cell or commit it to the repository. Copy `.env.example` to an untracked `.env`, or configure credentials in the shell that launches the application.

## Interpretation boundary

Successful execution demonstrates software behavior, tool boundaries, and learning concepts. It does not establish clinical correctness, comparative model superiority, or readiness for use with real patients.
