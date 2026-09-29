# Agentic Demos — Jupyter

These ten notebooks explain how agentic systems work, fail, and are governed in healthcare settings. They support clinical, operational, and technical participants: readers can inspect trajectories and make workflow decisions without programming, while technical users can modify the tools, policies, and experiments.

All examples are fictional or synthetic. Nothing in this folder is a clinical protocol or patient-care system.

## Notebooks

| # | Notebook | Focus |
|---:|---|---|
| 1 | `01_llm_vs_tool.ipynb` | Model reasoning versus deterministic tools |
| 2 | `02_minimal_agent_loop.ipynb` | Observe, act, receive feedback, and stop |
| 3 | `03_human_in_the_loop_gate.ipynb` | Code-enforced human authorization |
| 4 | `04_memory_and_stale_facts.ipynb` | Memory, provenance, and outdated facts |
| 5 | `05_tool_retrieval_and_routing.ipynb` | Tool selection and model routing |
| 6 | `06_uncertainty_and_abstention.ipynb` | Uncertainty, abstention, and escalation |
| 7 | `07_compounding_reliability.ipynb` | Reliability across complete trajectories |
| 8 | `08_orchestrator_and_specialists.ipynb` | Single-agent and multi-agent trade-offs |
| 9 | `09_fhir_sandbox_agent.ipynb` | A governed synthetic FHIR environment |
| 10 | `10_safety_prompt_injection.ipynb` | Prompt injection and architectural controls |

See [CURRICULUM_MAP.md](CURRICULUM_MAP.md) for suggested pathways and [INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md) for facilitation guidance.

## Run in Explore mode

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
export LAB_MODE=mock
jupyter lab
```

Open the notebooks in numerical order or choose one of the shorter workshop pathways in the curriculum map.

## Optional Live mode

Configure credentials in the shell that launches Jupyter; never paste an API key into a notebook.

```bash
export OPENAI_API_KEY="your-key"
export MODEL="your-model-id"
export LAB_MODE=live
jupyter lab
```

An OpenAI-compatible endpoint can optionally be selected with `OPENAI_BASE_URL`.

Notebook 6 intentionally retains 76 live calls. The resulting latency and token use are part of the exercise rather than overhead to hide. Live completion demonstrates authentic model interaction, not clinical correctness.

## Validate without an API key

```bash
python3 validate_lab.py
```

The validator removes API credentials and executes the notebooks in deterministic mode. For workshops, run it before participants arrive.

## Notebook pattern

Each notebook contains learning objectives, a safety notice, an executable demonstration, an exercise, simple configuration choices, an optional technical extension, observability information where a model is involved, and an interpretation boundary.
