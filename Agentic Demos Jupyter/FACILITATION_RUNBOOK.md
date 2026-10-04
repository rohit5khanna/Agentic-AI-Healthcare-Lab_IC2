# Facilitation runbook

This runbook is for a facilitator operating the Healthcare Agent Learning Lab. It does not turn the demonstrations into clinical decision support.

## Recommended live pathway

For a 90-minute guided session, use Notebooks 1, 2, 3, 6, and 9. The sequence moves from a single model call to a tool-using loop, an enforced human gate, repeated-sampling uncertainty, and a synthetic FHIR environment.

Notebook 6 intentionally performs 76 model calls. In the latest validation it took about 163 seconds and used 19,313 tokens. Keep the full run when latency is a teaching objective. Start it before the discussion about operational burden rather than leaving the group in silence.

## Before participants arrive

1. Create an isolated Python environment and install `requirements.txt`.
2. Run `python3 validate_lab.py`; require 10/10 passes.
3. If demonstrating a live model, launch Jupyter from a shell containing `OPENAI_API_KEY`, `MODEL`, and `LAB_MODE=live`. Never paste a key into a notebook.
4. Confirm that the first output in each model-using notebook says `Backend: REAL model = ...`. If it says mock, stop and label that run accurately.
5. Keep the redacted validated traces under `artifacts/live_validation/` available as a fallback if the provider or network is unavailable.
6. Use fictional or synthetic records only. The lab is not approved for patient care.

## Suggested timing

| Segment | Time | Activity |
|---|---:|---|
| Framing | 10 min | Define model, agent, tool, environment, trajectory, gate, and deployment rung. |
| Notebook 1 | 10 min | Compare plausible model arithmetic with a deterministic calculation. |
| Notebook 2 | 15 min | Trace perception, tool selection, observation, and stopping. |
| Notebook 3 | 15 min | Separate a model proposal from an authorized action. |
| Notebook 6 | 20 min | Run all 76 calls and discuss agreement, latency, cost, and abstention. |
| Notebook 9 | 15 min | Inspect synthetic FHIR reads and a denied write-back. |
| Close | 5 min | Capture one permitted workflow and one required human-review condition per group. |

## Facilitation rules

- Ask participants to predict the next action before running a cell.
- Discuss the trajectory and final system state, not only the prose answer.
- Do not promise that a live run will match a saved trace.
- Treat malformed arguments, extra calls, disagreement, and latency as observations—not embarrassment to hide.
- State when an output is mock, replayed, deterministic, or live.
- Do not equate a successful execution with clinical correctness.

## If something fails live

1. Preserve the error and identify whether it arose from the model, parser, tool, policy, network, or environment.
2. Show the corresponding redacted trace in `artifacts/live_validation/`.
3. Continue the design exercise using that trace.
4. Do not silently switch to mock output.

## What to collect

For each proposed use case, record the deployment rung, minimum evidence, allowed tools, prohibited actions, reviewer role, escalation condition, acceptable final state, and likely failure modes. These learning-session outputs are candidate requirements; they are not physician-approved ground truth.
