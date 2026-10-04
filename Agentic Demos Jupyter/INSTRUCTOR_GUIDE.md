# Instructor guide

## Purpose

The goal is not to persuade participants that an agent is clinically capable. The goal is to help them see the mechanisms, decisions, and failure modes clearly enough to contribute their workflow expertise.

Clinical participants are not “nontechnical users” in this lab. They are the experts on acceptable evidence, consequential actions, escalation, ambiguity, workload, and accountability.

## Before the learning session

1. Run `python3 validate_lab.py` with no API key.
2. Decide which exercises will be live and which will use mock or replay. Never present a mock or replay as a fresh model run.
3. Confirm that no real patient information appears in the notebooks or discussion materials.
4. Select the pathway from `CURRICULUM_MAP.md` rather than attempting all ten notebooks in a short session.
5. Prepare a visible definition of model, agent, tool, environment, trajectory, gate, and abstention.
6. If using live mode, budget for variable latency and keep a fallback replay trace for network failure. Notebook 6 intentionally makes all 76 calls; allow roughly three minutes for the calls alone.

## Facilitation pattern for each notebook

1. **Predict:** Ask participants what they expect the system to do.
2. **Observe:** Run the demonstration without explaining the result first.
3. **Trace:** Identify what information the system saw and which action occurred.
4. **Judge:** Ask whether the behavior is acceptable for the stated workflow.
5. **Redesign:** Ask what the environment should enforce.
6. **Generalize:** Connect the lesson to a workflow known by the group.

Avoid asking only, “Was the answer correct?” Also ask:

- Did the system have enough information?
- Did it use an appropriate tool?
- Was the action permitted?
- Was uncertainty visible?
- Did the workflow reach a safe final state?
- Who was accountable for the consequential decision?

## Notebook-specific teaching notes

### 1. LLM versus deterministic tool

Expected insight: deterministic arithmetic improves verifiability but does not validate the clinical premise, patient identity, units, or appropriateness. The notebook does not yet show autonomous model-selected tool calling.

### 2. Minimal agent loop

Expected insight: an agent is a control loop over state and tools, not merely a long response. Discuss maximum steps, repeated calls, malformed actions, and the difference between drafting and executing.

### 3. Human approval gate

Expected insight: the gate must be enforced in the action path. A person in the loop can still lack context, suffer automation bias, or lack the authority to approve. The fictional warfarin proposal is not a dosing recommendation.

### 4. Memory and stale facts

Expected insight: storing more information is not automatically better. Memory needs time, source, status, supersession, conflict resolution, and reverification rules.

### 5. Tool retrieval and routing

Expected insight: limiting tools can reduce risk, but omitting the required tool causes a different failure. Routing decisions should reflect consequence and uncertainty, not cost alone.

### 6. Uncertainty and abstention

Expected insight: agreement is not truth and is not calibrated probability. Abstention transfers work to someone else, so escalation quality and workload must be measured. Do not shorten the 76-call live exercise when latency is one of the teaching objectives; ask participants what that delay would mean inside a real workflow.

### 7. Compounding reliability

Expected insight: end-to-end outcomes can be worse than step-level results suggest. The simple product assumes independent errors; real failures may be correlated and have unequal consequences.

### 8. Orchestrators and specialists

Expected insight: multiple agents add calls, latency, handoffs, and disagreement. Use them only when separable work, different tools, permissions, or contexts justify the additional machinery.

### 9. FHIR sandbox

Expected insight: FHIR is a data exchange foundation, not a completed clinical environment. Production integration also requires patient scoping, terminology, profiles, authentication, authorization, provenance, audit, workflow ownership, and validation.

### 10. Prompt injection

Expected insight: retrieved text is untrusted input. A numeric policy and a human gate are illustrative layers, not a complete safety system; reviewers can also be manipulated.

## Capturing participant input

For each group, record:

- workflow or clinical domain;
- proposed agent task;
- minimum necessary evidence;
- allowed and prohibited actions;
- human-review point;
- abstention or escalation condition;
- likely failure cases;
- acceptable final state;
- unresolved question requiring domain review.

These outputs can later inform physician-authored task templates without treating learning-session discussion as validated clinical ground truth.

## Language to use

Prefer:

- “The demonstration shows…”
- “The scripted mock illustrates…”
- “The environment allowed or blocked…”
- “The agent’s trajectory contained…”
- “Clinical correctness has not been established.”

Avoid:

- “The agent understands the patient.”
- “The system is safe because a person approved it.”
- “High model confidence proves correctness.”
- “FHIR makes this ready for an EHR.”
- “The mock run proves the model can do this.”

## Closing discussion

Ask each participant to complete two sentences:

1. “I would permit an agent to ______ only if the environment enforced ______.”
2. “I would require human review when ______ because ______.”

The answers are useful inputs for later deployment-rung and task-template development.
