# Curriculum map

The notebooks are designed as a progression, but a workshop can select a shorter pathway.

## Full sequence

### Module A — What an agent is

1. **LLM versus deterministic tool** — introduces delegation and verifiability.
2. **Minimal agent loop** — makes state, tools, observations, and stopping visible.
3. **Human approval gate** — separates model proposals from authorized actions.

### Module B — What makes an agent unreliable

4. **Memory and stale facts** — shows temporal and provenance failures.
5. **Tool retrieval and routing** — introduces action-space and resource allocation decisions.
6. **Uncertainty and abstention** — connects uncertainty to escalation workflows.
7. **Compounding reliability** — shifts evaluation from individual steps to trajectories.

### Module C — System architecture and healthcare integration

8. **Orchestrators and specialists** — examines multi-agent trade-offs.
9. **FHIR sandbox** — connects the control loop to structured health records.
10. **Prompt injection** — demonstrates untrusted content and layered controls.

## Recommended workshop pathways

### 60-minute clinical introduction

- Notebook 2: minimal loop
- Notebook 3: human gate
- Notebook 4: stale memory
- Notebook 10: prompt injection

Use only the demonstration and clinical exercise in each notebook.

### 90-minute deployment-ladder workshop

- Notebook 1: tool versus model
- Notebook 2: minimal loop
- Notebook 3: human gate
- Notebook 6: abstention
- Notebook 9: FHIR sandbox

End by asking participants to place each demonstrated action on the project’s deployment ladder.

### Half-day design workshop

- Notebooks 1–7 in sequence
- Small-group workflow mapping
- Notebook 9 as the integration example
- Notebook 10 as the closing safety exercise

### Technical onboarding

- Run all ten notebooks in mock mode.
- Repeat selected notebooks with a live model.
- Complete each technical extension.
- Compare traces rather than final prose alone.

## Cross-cutting learning outcomes

By the end of the full sequence, participants should be able to:

- distinguish a model, an agent loop, a tool, and an environment;
- identify read-only, administrative, clinical-support, and consequential actions;
- explain why prompts do not enforce permissions;
- recognize stale state, missing context, and untrusted retrieved content;
- specify when an agent should abstain or request human review;
- compare single-agent and multi-agent architectures;
- interpret a basic tool trajectory and audit record;
- distinguish technical task completion from clinical correctness.

## Relationship to Barry

The learning lab decomposes the system into understandable mechanisms. Barry recombines those mechanisms in complete episodes over synthetic Synthea FHIR records.

The learning lab should be taught first when participants are unfamiliar with agentic systems. Barry can then serve as the applied demonstration showing how the pieces interact in a longer workflow.
