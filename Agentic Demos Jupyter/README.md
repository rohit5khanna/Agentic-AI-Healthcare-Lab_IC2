# Healthcare Agent Learning Lab — Jupyter Edition

This learning lab explains how agentic systems work, fail, and are governed in healthcare settings. It is deliberately separate from the Barry/Synthea applied-use-case pilot.

The ten notebooks support two audiences at the same time:

- **Clinical and operational participants** inspect trajectories, make workflow and safety decisions, change simple values, and discuss accountability without needing to program.
- **Technical participants** can inspect the implementation, modify tools and policies, introduce failures, and extend the experiments.

All examples are fictional or synthetic. Nothing in this repository is a clinical protocol or a patient-care system.

## Curriculum

| # | Notebook | Central question |
|---:|---|---|
| 1 | LLM versus deterministic tool | Which work belongs to language generation, retrieval, tools, or people? |
| 2 | Minimal agent loop | What makes an agent different from a single model response? |
| 3 | Human approval gate | How can consequential actions be stopped by architecture? |
| 4 | Memory and stale facts | What happens when remembered information is no longer current? |
| 5 | Tool retrieval and routing | Which tools and models should be available for a task? |
| 6 | Uncertainty and abstention | When should the system stop and escalate? |
| 7 | Compounding reliability | Why can reliable-looking steps produce an unreliable workflow? |
| 8 | Orchestrators and specialists | When does a multi-agent design justify its complexity? |
| 9 | FHIR sandbox | How do patient records become an agent environment? |
| 10 | Prompt injection | Why must safety live outside the prompt? |

See [CURRICULUM_MAP.md](CURRICULUM_MAP.md) for sequencing and [INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md) for facilitation guidance.

The proposed participant-facing Marimo edition is described in [MARIMO_IMPLEMENTATION_PLAN.md](MARIMO_IMPLEMENTATION_PLAN.md). It is a planned companion experience, not a replacement for these Jupyter notebooks.

## Three execution modes

The notebooks distinguish three kinds of evidence:

1. **Mock mode** — scripted, deterministic behavior for teaching system structure. It requires no API key.
2. **Replay** — a previously recorded trajectory discussed as a case. Replay material may be added without making a new model call.
3. **Live mode** — an actual model call whose output may vary and may incur cost.

A scripted mock output must never be presented as measured model performance. Mode selection is explicit: the model-using notebooks stop unless `LAB_MODE` is set to `mock` or `live`.

## Quick start

The notebooks themselves use the Python standard library in mock mode, except for the visualization in Notebook 7.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
export LAB_MODE=mock
jupyter lab
```

Open the notebooks in numerical order. Before a guided session, the instructor should run the validation command before participants arrive:

```bash
python3 validate_lab.py
```

The validator deliberately removes API credentials and executes the code cells in mock mode.

## Optional live-model mode

Live mode is not required for the core learning sequence. If the facilitator chooses to use it, set the model configuration in the shell that launches Jupyter. Do not paste credentials into a notebook.

```bash
export OPENAI_API_KEY="your-key"
export MODEL="your-model-id"
export LAB_MODE=live
jupyter lab
```

An OpenAI-compatible endpoint can optionally be selected with `OPENAI_BASE_URL`. The current notebooks use a transparent text/JSON loop for teaching. They do not yet demonstrate provider-native tool calling.

For group sessions, use mock or replay mode for participant machines and reserve live mode for a facilitator-controlled demonstration. This prevents credential exposure, unpredictable costs, and network-dependent failures.

## Live validation

The local validation runner can reuse Barry's `.env` without printing or copying the key:

```bash
python3 live_validate_lab.py
```

Set `LEARNING_LAB_ENV_FILE` to use a different environment file. The runner forces the FHIR notebook to use its local synthetic bundle and denies gated actions. It writes redacted logs and a report under `artifacts/live_validation/`.

The current live-validation report is available at `artifacts/live_validation/live_validation_report.md`. Completion confirms that genuine model calls occurred and the notebook finished; it is not a clinical-correctness score.

Notebook 6 intentionally retains 76 live calls. The elapsed time and estimated cost are outputs of the exercise, not incidental overhead to hide. A separate repeatability smoke test for selected agent notebooks can be run with `python3 repeatability_check.py`; its redacted report is written under `artifacts/repeatability/`.

## Notebook pattern

Every notebook follows the same progression:

1. Learning objectives and safety notice
2. Concept explanation
3. Executable demonstration
4. Clinical and operational exercise
5. Simple “try it” configuration cell
6. Optional technical extension
7. Observability summary where a model is involved
8. Interpretation boundary and exit question

The observability wrapper records model calls, latency, response IDs, input and output tokens, cached and reasoning tokens when supplied by the provider, provider-reported cost when available, and an explicitly labeled cost estimate for the configured teaching model. Provider billing remains authoritative.

## Rebuilding the notebooks

The reviewed source notebooks remain untouched in `../tmp/agent_demos_review`. The expanded notebooks are generated reproducibly:

```bash
python3 build_lab.py
python3 validate_lab.py
```

Do not edit generated notebooks and then rerun the builder without first moving the intended changes into `build_lab.py`, or the generated edits will be overwritten.

## Scope boundary

This repository teaches components and design decisions. Barry is the separate applied environment that combines these ideas with Synthea FHIR records and deployment-rung scenarios.

Neither project currently establishes clinical accuracy, comparative model superiority, or readiness for real patient care.
