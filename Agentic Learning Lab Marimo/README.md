# Healthcare Agent Learning Lab — Marimo Edition

This is the participant-facing companion to the ten-notebook Jupyter learning lab. It is one Marimo notebook/application with a dedicated Home page and an app-controlled curriculum menu for choosing among all ten demonstrations. The panel fully hides and the learning canvas reflows when the participant selects **Curriculum**.

Home introduces the agent–tool–environment–human relationship, the four curriculum perspectives, the standard learning sequence, and the Explore, Replay, and Live modes. Every demonstration is permanently visible in the menu and can be opened with one click; navigation never executes a model call.

The unified application provides interactive translations of all ten Jupyter demonstrations:

- Demo 1: LLM versus deterministic tool
- Demo 2: Minimal agent loop
- Demo 3: Human approval gate
- Demo 4: Memory, provenance, and stale facts
- Demo 5: Tool retrieval and model routing
- Demo 6: Uncertainty and abstention, including the full 76-interaction experiment
- Demo 7: Compounding reliability
- Demo 8: Orchestrator and specialist agents
- Demo 9: Synthetic FHIR sandbox
- Demo 10: Prompt injection and architectural safety

All cases are fictional or synthetic. The application is for research and education only and must not be used for patient care.

## Run the participant application

```bash
cd "/Users/rohitkhanna/Desktop/AI Agent Healthcare_IC2/agent_learning_lab_marimo"
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
marimo run healthcare_agent_learning_lab.py
```

## Open the technical editor

```bash
marimo edit healthcare_agent_learning_lab.py
```

## Execution modes

- **Explore:** deterministic teaching behavior; no API key required.
- **Replay:** clearly labelled saved or deterministic trace behavior; no new API call.
- **Live:** genuine model calls for model-based modules. The routing and compounding-reliability modules remain explicitly deterministic. Requires `OPENAI_API_KEY` and `MODEL` in the server environment when calls are needed.

Demo 6 intentionally performs all 76 sequential calls in Live mode. Its latency, token use, and cost are part of the learning experience rather than overhead to hide.

Changing curriculum controls never initiates a model call. A run starts only when the participant presses **Run this demonstration**.

## Participant experience

Each translated demonstration now follows a visible learning story:

1. Understand a synthetic case and why it matters.
2. See the intended model–tool–environment–human flow.
3. Predict the agent's first action.
4. Run and inspect a color-coded trajectory, one step at a time.
5. Compare the prediction with the observed behavior.
6. Inspect the governed final environment state.
7. Judge the trajectory and propose a safer redesign.

The raw table and JSON state remain available in a collapsed technical section, but they are no longer the primary participant view.

## Test

```bash
python3 -m unittest -v test_lab_core.py
marimo check healthcare_agent_learning_lab.py
```

An optional live smoke test reuses Barry's local `.env` without printing or copying the key:

```bash
python3 live_smoke_test.py
```

It writes redacted technical results under `artifacts/`.

The Jupyter edition remains the canonical detailed technical curriculum during this pilot. Content changes should be compared across both editions before the Marimo application is considered final.
