# Agentic Learning Lab — Marimo

This is the participant-facing companion to the ten Jupyter notebooks. It is a single Marimo application with a Home page and a curriculum menu for choosing among all ten demonstrations.

Home introduces the agent–tool–environment–human relationship, four curriculum perspectives, the learning sequence, and the Explore, Replay, and Live modes. Navigation never executes a model call.

All cases are fictional or synthetic. The application is for research and education only and must not be used for patient care.

## Run the application

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
marimo run healthcare_agent_learning_lab.py
```

To inspect or modify the implementation:

```bash
marimo edit healthcare_agent_learning_lab.py
```

## Execution modes

- **Explore:** deterministic teaching behavior; no API key required.
- **Replay:** clearly labelled representative trace behavior; no new model call.
- **Live:** genuine model calls for model-based demonstrations. It requires `OPENAI_API_KEY` and `MODEL` in the server environment.

Demo 6 intentionally performs all 76 sequential calls in Live mode. Its latency, token use, and cost are part of the workshop lesson.

Changing curriculum controls never initiates a model call. A run starts only when the participant presses **Run this demonstration**.

## Test

```bash
python3 -m unittest -v test_lab_core.py
marimo check healthcare_agent_learning_lab.py
```

For an optional live smoke test, create an untracked `.env` using the repository's `.env.example`, then run:

```bash
python3 live_smoke_test.py
```

The smoke test writes redacted results under `artifacts/`, which is excluded from Git. A pass confirms authentic model interaction ending in normal completion or safe containment; it does not establish clinical correctness or safety.
