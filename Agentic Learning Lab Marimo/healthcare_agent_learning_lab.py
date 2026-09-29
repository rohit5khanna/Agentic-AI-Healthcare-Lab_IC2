import marimo

__generated_with = "0.20.4"
app = marimo.App(width="full")


@app.cell
def _():
    import html
    import json
    import time

    import marimo as mo

    from lab_core import CASE_CARDS, CATALOG_BY_ID, DEMO_CATALOG, run_demo

    return CASE_CARDS, CATALOG_BY_ID, DEMO_CATALOG, html, json, mo, run_demo, time


@app.cell
def _(DEMO_CATALOG, mo):
    _menu_titles = {
        "01": "Model vs calculator",
        "02": "Minimal agent loop",
        "03": "Human approval gate",
        "04": "Memory & stale facts",
        "05": "Tool retrieval & routing",
        "06": "Uncertainty & abstention",
        "07": "Compounding reliability",
        "08": "Orchestrator & specialists",
        "09": "FHIR sandbox tools",
        "10": "Prompt injection safety",
    }
    _menu_labels = ["⌂  Home"] + [
        f"{demo.id}  ·  {_menu_titles[demo.id]}" for demo in DEMO_CATALOG
    ]
    menu_label_to_id = {"⌂  Home": None}
    menu_label_to_id.update(
        {
            f"{demo.id}  ·  {_menu_titles[demo.id]}": demo.id
            for demo in DEMO_CATALOG
        }
    )
    curriculum_menu = mo.ui.radio(
        options=_menu_labels,
        value="⌂  Home",
        label="",
        inline=False,
    )
    mode_selector = mo.ui.radio(
        options=["Explore", "Replay", "Live"],
        value="Explore",
        label="Execution mode",
        inline=True,
    )
    gate_decision = mo.ui.radio(
        options=["Reject", "Request more information", "Approve"],
        value="Request more information",
        label="Human decision for gated actions",
    )
    evidence_selector = mo.ui.multiselect(
        options=[
            "Latest INR",
            "Current medication",
            "Bleeding assessment",
            "Prescriber identity",
        ],
        value=["Latest INR", "Current medication"],
        label="Evidence available to the reviewer",
        full_width=True,
    )
    memory_policy = mo.ui.radio(
        options=["Compare both", "Naive", "Current"],
        value="Compare both",
        label="Memory recall policy",
    )
    tool_query = mo.ui.dropdown(
        options=[
            "get the most recent INR and the current medications",
            "schedule a follow-up appointment and message the patient",
            "reconcile medications for a warfarin interaction",
        ],
        value="get the most recent INR and the current medications",
        label="Task used to retrieve tools",
        full_width=True,
    )
    tool_limit = mo.ui.slider(
        start=1,
        stop=6,
        step=1,
        value=3,
        label="Maximum tools exposed",
        show_value=True,
        full_width=True,
    )
    abstention_threshold = mo.ui.slider(
        start=0.5,
        stop=0.9,
        step=0.1,
        value=0.7,
        label="Agreement threshold for answering",
        show_value=True,
        full_width=True,
    )
    per_step_reliability = mo.ui.slider(
        start=0.8,
        stop=0.99,
        step=0.01,
        value=0.95,
        label="Per-step reliability",
        show_value=True,
        full_width=True,
    )
    chain_length = mo.ui.slider(
        start=3,
        stop=8,
        step=1,
        value=5,
        label="Workflow steps",
        show_value=True,
        full_width=True,
    )
    verifier_coverage = mo.ui.slider(
        start=0.0,
        stop=0.95,
        step=0.05,
        value=0.0,
        label="Share of step errors caught by a verifier",
        show_value=True,
        full_width=True,
    )
    architecture_selector = mo.ui.radio(
        options=["Compare both", "Multi-agent", "Single agent"],
        value="Compare both",
        label="Architecture to run",
    )
    prediction_selector = mo.ui.radio(
        options=[
            "Retrieve evidence first",
            "Draft a proposal for review",
            "Attempt a record change",
            "Escalate immediately",
        ],
        value="Retrieve evidence first",
        label="What should the agent do first?",
    )
    judgment_selector = mo.ui.radio(
        options=["Acceptable", "Unacceptable", "Uncertain"],
        value="Uncertain",
        label="How would you judge this trajectory?",
        inline=True,
    )
    reflection_input = mo.ui.text_area(
        label="What would you change in the environment?",
        placeholder="For example: restrict a tool, require another fact, or add a human gate…",
        full_width=True,
    )
    navigation_toggle = mo.ui.button(
        value=True,
        on_click=lambda shown: not shown,
        label="☰  Curriculum",
        kind="neutral",
        tooltip="Show or hide the curriculum controls.",
    )
    return (
        abstention_threshold,
        architecture_selector,
        chain_length,
        curriculum_menu,
        evidence_selector,
        gate_decision,
        judgment_selector,
        menu_label_to_id,
        memory_policy,
        mode_selector,
        navigation_toggle,
        per_step_reliability,
        prediction_selector,
        reflection_input,
        tool_limit,
        tool_query,
        verifier_coverage,
    )


@app.cell
def _(html, json, mo):
    _colors = {
        "read": ("#2563eb", "#eff6ff", "READ"),
        "draft": ("#7c3aed", "#f5f3ff", "DRAFT"),
        "write": ("#c2410c", "#fff7ed", "PROPOSED WRITE"),
        "blocked": ("#b91c1c", "#fef2f2", "BLOCKED"),
        "final": ("#047857", "#ecfdf5", "FINAL"),
        "model": ("#475569", "#f8fafc", "MODEL"),
    }

    def panel(
        items,
        accent="#2563eb",
        background="#ffffff",
        padding="1.2rem",
        fill_height=False,
    ):
        styles = {
            "background": background,
            "border": "1px solid #e2e8f0",
            "border-left": f"4px solid {accent}",
            "border-radius": "16px",
            "padding": padding,
            "box-shadow": "0 8px 24px rgba(15, 23, 42, 0.055)",
        }
        if fill_height:
            styles.update({"height": "100%", "box-sizing": "border-box"})
        return mo.vstack(items, gap=0.8).style(styles)

    def badge(text, foreground="#1d4ed8", background="#dbeafe"):
        return mo.Html(
            f'<span style="display:inline-block;padding:.28rem .58rem;border-radius:999px;'
            f'background:{background};color:{foreground};font-size:.72rem;font-weight:800;'
            f'letter-spacing:.055em;text-transform:uppercase">{html.escape(str(text))}</span>'
        )

    def _action_style(action, status):
        lowered = action.lower()
        if status == "blocked" or "invalid" in lowered:
            return _colors["blocked"]
        if lowered == "final":
            return _colors["final"]
        if lowered.startswith("get_") or "calculator" in lowered:
            return _colors["read"]
        if lowered.startswith("draft") or "model_response" in lowered:
            return _colors["draft"]
        if lowered.startswith("write") or "change" in lowered:
            return _colors["write"]
        return _colors["model"]

    def _pretty(value):
        return html.escape(json.dumps(value, ensure_ascii=False, indent=2))

    def trace_card(step):
        foreground, background, label = _action_style(step.action, step.status)
        plan = html.escape(step.thought or "No rationale was supplied.")
        action = html.escape(step.action)
        observation = _pretty(step.observation)
        action_input = _pretty(step.action_input)
        return mo.Html(
            f"""
            <section style="position:relative;margin-left:1.1rem;padding:0 0 1.15rem 1.55rem;
                            border-left:2px solid #cbd5e1">
              <div style="position:absolute;left:-.62rem;top:.1rem;width:1.12rem;height:1.12rem;
                          border-radius:50%;background:{foreground};border:3px solid white;
                          box-shadow:0 0 0 1px #cbd5e1"></div>
              <div style="border:1px solid #e2e8f0;border-radius:14px;background:white;
                          box-shadow:0 5px 16px rgba(15,23,42,.045);overflow:hidden">
                <div style="padding:.75rem 1rem;background:{background};display:flex;gap:.65rem;
                            align-items:center;justify-content:space-between;flex-wrap:wrap">
                  <div><span style="font-size:.72rem;font-weight:800;color:{foreground};
                              letter-spacing:.06em">STEP {step.step + 1} · {label}</span>
                       <strong style="display:block;color:#0f172a;margin-top:.14rem">{action}</strong></div>
                  <span style="font-size:.75rem;color:{foreground};font-weight:700">{html.escape(step.status.upper())}</span>
                </div>
                <div style="padding:.9rem 1rem;color:#334155">
                  <div style="font-size:.78rem;font-weight:800;color:#64748b;text-transform:uppercase;
                              letter-spacing:.05em">Agent's stated plan</div>
                  <div style="margin:.25rem 0 .8rem;line-height:1.5">{plan}</div>
                  <details>
                    <summary style="cursor:pointer;color:{foreground};font-weight:700">Inspect input and environment response</summary>
                    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.75rem;margin-top:.7rem">
                      <div><div style="font-size:.72rem;font-weight:800;color:#64748b">ACTION INPUT</div>
                           <pre style="white-space:pre-wrap;background:#f8fafc;padding:.65rem;border-radius:8px;font-size:.78rem">{action_input}</pre></div>
                      <div><div style="font-size:.72rem;font-weight:800;color:#64748b">ENVIRONMENT RESPONSE</div>
                           <pre style="white-space:pre-wrap;background:#f8fafc;padding:.65rem;border-radius:8px;font-size:.78rem">{observation}</pre></div>
                    </div>
                  </details>
                </div>
              </div>
            </section>
            """
        )

    def flow_map(stages):
        pieces = []
        for index, stage in enumerate(stages):
            pieces.append(
                f'<div style="flex:1 1 125px;min-width:110px;border:1px solid #cbd5e1;'
                f'border-radius:12px;padding:.75rem;background:white;text-align:center">'
                f'<div style="color:#2563eb;font-weight:800;font-size:.72rem">{index + 1}</div>'
                f'<div style="font-weight:700;color:#1e293b;margin-top:.2rem">{html.escape(stage)}</div></div>'
            )
            if index < len(stages) - 1:
                pieces.append(
                    '<div style="color:#94a3b8;font-size:1.3rem;align-self:center">→</div>'
                )
        return mo.Html(
            '<div style="display:flex;align-items:stretch;gap:.5rem;flex-wrap:wrap">'
            + "".join(pieces)
            + "</div>"
        )

    def state_card(state):
        rows = []
        for key, value in state.items():
            if isinstance(value, bool):
                rendered = "Yes" if value else "No"
            elif isinstance(value, (list, dict)):
                rendered = f"<pre style='white-space:pre-wrap;margin:0;font-size:.78rem'>{_pretty(value)}</pre>"
            else:
                rendered = html.escape(str(value))
            rows.append(
                f'<div style="padding:.8rem 0;border-bottom:1px solid #e2e8f0">'
                f'<div style="font-size:.72rem;font-weight:800;color:#64748b;text-transform:uppercase;letter-spacing:.05em">{html.escape(str(key))}</div>'
                f'<div style="color:#0f172a;margin-top:.2rem">{rendered}</div></div>'
            )
        return mo.Html("<div>" + "".join(rows) + "</div>")

    return badge, flow_map, panel, state_card, trace_card


@app.cell
def _(CATALOG_BY_ID, CASE_CARDS, curriculum_menu, menu_label_to_id):
    selected_id = menu_label_to_id[curriculum_menu.value]
    _content_id = selected_id or "01"
    selected_demo = CATALOG_BY_ID[_content_id]
    selected_case = CASE_CARDS[_content_id]
    return selected_case, selected_demo, selected_id


@app.cell
def _(
    abstention_threshold,
    architecture_selector,
    chain_length,
    evidence_selector,
    gate_decision,
    memory_policy,
    mode_selector,
    mo,
    per_step_reliability,
    prediction_selector,
    selected_id,
    time,
    tool_limit,
    tool_query,
    verifier_coverage,
):
    run_button = mo.ui.button(
        value=None,
        on_click=lambda _value: {
            "nonce": time.time_ns(),
            "demo_id": selected_id,
            "mode": mode_selector.value,
            "gate_decision": gate_decision.value,
            "evidence": list(evidence_selector.value),
            "prediction": prediction_selector.value,
            "parameters": {
                "memory_policy": memory_policy.value,
                "tool_query": tool_query.value,
                "tool_limit": tool_limit.value,
                "abstention_threshold": abstention_threshold.value,
                "per_step_reliability": per_step_reliability.value,
                "chain_length": chain_length.value,
                "verifier_coverage": verifier_coverage.value,
                "architecture": architecture_selector.value,
            },
        },
        label="▶  Run this demonstration",
        kind="success",
        full_width=True,
        tooltip="Only this button can start a demonstration or live model call.",
    )
    return run_button


@app.cell
def _(mo, run_button, run_demo):
    request = run_button.value
    if request is None:
        run_result = None
        run_error = None
    else:
        try:
            with mo.status.spinner(title="Running the selected demonstration…"):
                run_result = run_demo(
                    request["demo_id"],
                    request["mode"],
                    gate_decision=request["gate_decision"],
                    evidence=request["evidence"],
                    parameters=request["parameters"],
                )
            run_error = None
        except Exception as exc:
            run_result = None
            run_error = f"{type(exc).__name__}: {exc}"
    return request, run_error, run_result


@app.cell
def _(
    abstention_threshold,
    architecture_selector,
    badge,
    chain_length,
    curriculum_menu,
    evidence_selector,
    gate_decision,
    memory_policy,
    mode_selector,
    mo,
    panel,
    per_step_reliability,
    run_button,
    selected_demo,
    selected_id,
    tool_limit,
    tool_query,
    verifier_coverage,
):
    _demo_controls = []
    if selected_id in {"03", "09", "10"}:
        _demo_controls.append(gate_decision)
    if selected_id == "03":
        _demo_controls.append(evidence_selector)
    elif selected_id == "04":
        _demo_controls.append(memory_policy)
    elif selected_id == "05":
        _demo_controls.extend([tool_query, tool_limit])
    elif selected_id == "06":
        _demo_controls.append(abstention_threshold)
        if mode_selector.value == "Live":
            _demo_controls.append(
                mo.callout(
                    "Live mode intentionally makes all 76 sequential model calls. Expect several minutes of visible latency and API usage.",
                    kind="warn",
                )
            )
    elif selected_id == "07":
        _demo_controls.extend(
            [per_step_reliability, chain_length, verifier_coverage]
        )
    elif selected_id == "08":
        _demo_controls.append(architecture_selector)
    if selected_id in {"05", "07"} and mode_selector.value == "Live":
        _demo_controls.append(
            mo.callout(
                "This demonstration is intentionally deterministic; Live mode will not make a model call.",
                kind="info",
            )
        )
    _status = badge("Interactive", "#047857", "#d1fae5")
    _viewing_label = (
        "Home"
        if selected_id is None
        else f"Demo {selected_id} · {selected_demo.title}"
    )
    _menu_items = [
        curriculum_menu,
        mo.hstack(
            [
                mo.Html(
                    '<span style="color:#64748b;font-size:.74rem;font-weight:750">VIEWING</span>'
                ),
                badge(_viewing_label),
            ],
            justify="space-between",
            gap=0.4,
            wrap=True,
        ),
    ]
    _execution_controls = []
    if selected_id is not None:
        _execution_controls = [
            mo.md("---\n#### Run controls"),
            mode_selector,
            *_demo_controls,
            run_button,
            mo.callout(
                "Changing a menu selection or control never starts a model call. Only the green run button executes the demonstration.",
                kind="info",
            ),
            mo.md(
                "**Mode guide**  \n"
                "Explore = deterministic teaching run  \n"
                "Replay = preserved behavior  \n"
                "Live = authentic model response"
            ),
        ]
    else:
        _execution_controls = [
            mo.callout(
                "Choose any demonstration from the menu when you are ready. Nothing runs until you press its green run button.",
                kind="info",
            )
        ]
    navigation_panel = panel(
        [
            mo.md("## Healthcare Agent Lab\n**One curriculum · ten demonstrations**"),
            _status,
            mo.md("### Explore the curriculum"),
            *_menu_items,
            *_execution_controls,
        ],
        accent="#0f766e",
        background="#f8fafc",
        padding="1rem",
    ).style(
        {
            "position": "sticky",
            "top": "1rem",
            "max-height": "calc(100vh - 2rem)",
            "overflow-y": "auto",
        }
    )
    return navigation_panel


@app.cell
def _(badge, flow_map, mo, panel):
    home_view = mo.vstack(
        [
            panel(
                [
                    mo.hstack(
                        [
                            badge("Welcome to the lab"),
                            badge("Synthetic cases", "#047857", "#d1fae5"),
                        ],
                        justify="space-between",
                        gap=0.5,
                        wrap=True,
                    ),
                    mo.md(
                        "# See how healthcare agents actually work\n"
                        "### Ten interactive demonstrations about models, tools, environments, memory, uncertainty, human gates, and safety."
                    ),
                    mo.md(
                        "This is not a gallery of polished AI answers. It is a learning environment for watching "
                        "**what an agent decides, which capability it invokes, what the environment returns, and where the system stops it.**"
                    ),
                ],
                accent="#2563eb",
                background="linear-gradient(135deg, #dbeafe 0%, #ffffff 62%, #f0fdfa 100%)",
                padding="1.7rem",
            ),
            mo.hstack(
                [
                    mo.stat("10", label="Interactive demonstrations", bordered=True),
                    mo.stat("3", label="Execution modes", bordered=True),
                    mo.stat("76", label="Calls in the full uncertainty lab", bordered=True),
                    mo.stat("0", label="Real patient records", bordered=True),
                ],
                widths="equal",
                gap=0.8,
                wrap=True,
            ),
            panel(
                [
                    mo.md(
                        "## What do we mean by an agent?\n"
                        "An agent is not simply an LLM producing a response. In these demonstrations, it is a system that can observe a case, choose an action, call a constrained tool, receive an environment response, and decide what to do next."
                    ),
                    flow_map(
                        [
                            "Observe the case",
                            "Choose an action",
                            "Call a tool",
                            "Environment responds",
                            "Stop, escalate, or continue",
                        ]
                    ),
                    mo.callout(
                        "The model can propose. The environment determines what is possible. Human authorization remains explicit for consequential actions.",
                        kind="info",
                    ),
                ],
                accent="#0f766e",
            ),
            mo.md("## Four perspectives you will explore"),
            mo.hstack(
                [
                    panel(
                        [
                            mo.md(
                                "### ① Fundamentals\n"
                                "Separate model reasoning from deterministic tools, follow a minimal agent loop, and inspect a code-enforced human gate."
                            ),
                        ],
                        accent="#2563eb",
                        fill_height=True,
                    ).style({"height": "100%", "min-height": "170px"}),
                    panel(
                        [
                            mo.md(
                                "### ② Reliability\n"
                                "See stale memory, tool retrieval, abstention, and compounding errors across an entire trajectory."
                            ),
                        ],
                        accent="#d97706",
                        fill_height=True,
                    ).style({"height": "100%", "min-height": "170px"}),
                    panel(
                        [
                            mo.md(
                                "### ③ Architecture\n"
                                "Compare one agent with specialist agents and connect governed tools to a synthetic FHIR record."
                            ),
                        ],
                        accent="#7c3aed",
                        fill_height=True,
                    ).style({"height": "100%", "min-height": "170px"}),
                    panel(
                        [
                            mo.md(
                                "### ④ Safety\n"
                                "Watch untrusted content influence a model while schemas, policies, permissions, and human gates contain the proposal."
                            ),
                        ],
                        accent="#b91c1c",
                        fill_height=True,
                    ).style({"height": "100%", "min-height": "170px"}),
                ],
                widths="equal",
                gap=0.8,
                wrap=True,
                align="stretch",
            ),
            panel(
                [
                    mo.md("## How to use each demonstration"),
                    flow_map(["Understand", "Predict", "Run", "Inspect", "Judge + redesign"]),
                    mo.md(
                        "Choose a demonstration from the curriculum menu. Make a prediction before running it, then compare your expectation with the observed trajectory—not only with the final answer."
                    ),
                ],
                accent="#64748b",
                background="#f8fafc",
            ),
            mo.hstack(
                [
                    panel(
                        [
                            mo.md(
                                "### Explore\n"
                                "Reproducible teaching behavior with no API key. Best for facilitated discussion and learning the structure."
                            )
                        ],
                        accent="#047857",
                        background="#f0fdf4",
                        fill_height=True,
                    ).style({"height": "100%", "min-height": "155px"}),
                    panel(
                        [
                            mo.md(
                                "### Replay\n"
                                "Preserved representative behavior with no new call. Useful when workshop connectivity or timing is limited."
                            )
                        ],
                        accent="#7c3aed",
                        background="#faf5ff",
                        fill_height=True,
                    ).style({"height": "100%", "min-height": "155px"}),
                    panel(
                        [
                            mo.md(
                                "### Live\n"
                                "Authentic model behavior with visible latency, token use, and safe containment of malformed or unexpected proposals."
                            )
                        ],
                        accent="#c2410c",
                        background="#fff7ed",
                        fill_height=True,
                    ).style({"height": "100%", "min-height": "155px"}),
                ],
                widths="equal",
                gap=0.8,
                wrap=True,
                align="stretch",
            ),
            panel(
                [
                    mo.md(
                        "## Ready to begin?\n"
                        "Select any numbered demonstration from the menu. A selection only changes the page; it cannot make an API call or modify an environment."
                    ),
                    mo.callout(
                        "Research and education only. Every case is fictional or synthetic and must not be used for patient care.",
                        kind="warn",
                    ),
                ],
                accent="#0f172a",
                background="#f8fafc",
            ),
        ],
        gap=1,
    )
    return home_view


@app.cell
def _(
    badge,
    flow_map,
    mo,
    panel,
    prediction_selector,
    selected_case,
    selected_demo,
):
    _implementation = (
        badge("Ready to run", "#047857", "#d1fae5")
        if selected_demo.implemented
        else badge("Design preview", "#92400e", "#fef3c7")
    )
    _facts = "\n".join(f"- {fact}" for fact in selected_case["facts"])
    intro_view = mo.vstack(
        [
            panel(
                [
                    mo.hstack(
                        [
                            badge(f"Demo {selected_demo.id} · {selected_demo.group}"),
                            _implementation,
                        ],
                        justify="space-between",
                        gap=0.5,
                        wrap=True,
                    ),
                    mo.md(
                        f"# {selected_demo.title}\n"
                        f"### {selected_demo.question}"
                    ),
                    mo.md(
                        "This lab follows the *behavior of a system*, not only the quality of its final sentence."
                    ),
                ],
                accent="#2563eb",
                background="linear-gradient(135deg, #eff6ff 0%, #ffffff 72%)",
                padding="1.5rem",
            ),
            mo.hstack(
                [
                    panel(
                        [
                            mo.md(f"### Synthetic case\n**{selected_case['title']}**\n\n{_facts}"),
                        ],
                        accent="#0f766e",
                    ),
                    panel(
                        [
                            mo.md("### Why this case matters"),
                            mo.md(selected_case["why"]),
                            mo.md(
                                "**What to watch:** Which decisions belong to the model, the tool, the environment, and the human?"
                            ),
                        ],
                        accent="#7c3aed",
                    ),
                ],
                widths="equal",
                gap=1,
                wrap=True,
                align="stretch",
            ),
            panel(
                [mo.md("### The path you are about to inspect"), flow_map(selected_case["flow"])],
                accent="#64748b",
                background="#f8fafc",
            ),
            panel(
                [
                    mo.md(
                        "### 1 · Predict before running\n"
                        "Commit to an expectation. The useful discussion begins when the observed trajectory differs from it."
                    ),
                    prediction_selector,
                ],
                accent="#d97706",
                background="#fffbeb",
            ),
        ],
        gap=1,
    )
    return intro_view


@app.cell
def _(
    badge,
    judgment_selector,
    mo,
    panel,
    reflection_input,
    request,
    run_error,
    run_result,
    selected_demo,
    selected_id,
    state_card,
    trace_card,
):
    if request is None or request["demo_id"] != selected_id:
        observed_view = panel(
            [
                mo.md(
                    "### 2 · Run and observe\n"
                    "No trajectory is displayed yet. Choose your prediction, then press the green run button in the curriculum panel."
                ),
                mo.callout(
                    "The run will reveal each model decision, tool call, environment response, gate, and final state in sequence.",
                    kind="info",
                ),
            ],
            accent="#94a3b8",
            background="#f8fafc",
        )
    elif run_error:
        observed_view = panel(
            [
                mo.md("### 2 · Run and observe"),
                mo.callout(
                    "The run ended in a contained error. No action was executed silently.",
                    kind="danger",
                ),
                mo.md(f"```text\n{run_error}\n```"),
            ],
            accent="#b91c1c",
            background="#fef2f2",
        )
    else:
        _telemetry = run_result.telemetry_summary()
        _status_badge = (
            badge(run_result.status, "#047857", "#d1fae5")
            if run_result.status == "completed"
            else badge(run_result.status, "#b91c1c", "#fee2e2")
        )
        _trace = (
            mo.vstack([trace_card(step) for step in run_result.trace], gap=0)
            if run_result.trace
            else mo.callout(
                "This curriculum entry is visible, but its interactive translation has not been implemented. No model call was made.",
                kind="warn",
            )
        )
        _warnings = (
            mo.vstack([mo.callout(item, kind="warn") for item in run_result.warnings])
            if run_result.warnings
            else mo.md("")
        )
        _first_action = run_result.trace[0].action if run_result.trace else "No action"
        _comparison = mo.callout(
            mo.md(
                f"You predicted **{request['prediction']}**. "
                f"The first observed action was **{_first_action}**."
            ),
            kind="success" if _first_action.startswith("get_") and "Retrieve" in request["prediction"] else "info",
        )
        _stats = mo.hstack(
            [
                mo.stat(len(run_result.trace), label="Trace steps", bordered=True),
                mo.stat(_telemetry["New live calls"], label="Live calls", bordered=True),
                mo.stat(_telemetry["Latency (s)"], label="Latency (s)", bordered=True),
                mo.stat(_telemetry["Tokens"], label="Tokens", bordered=True),
                mo.stat(_telemetry["Estimated cost (USD)"], label="Est. cost (USD)", bordered=True),
            ],
            widths="equal",
            gap=0.7,
            wrap=True,
        )
        _technical = mo.accordion(
            {
                "Technical trace and raw state": mo.vstack(
                    [
                        mo.ui.table(
                            run_result.trace_rows(),
                            selection=None,
                            pagination=False,
                            show_download=True,
                            wrapped_columns=["Plan", "Action input", "Observation"],
                        ),
                        mo.md("**Raw final state**"),
                        mo.tree(run_result.final_state),
                    ],
                    gap=0.8,
                )
            }
        )
        observed_view = mo.vstack(
            [
                panel(
                    [
                        mo.hstack(
                            [
                                mo.md("### 2 · Observed run"),
                                mo.hstack(
                                    [badge(request["mode"]), _status_badge],
                                    gap=0.4,
                                    wrap=True,
                                ),
                            ],
                            justify="space-between",
                            wrap=True,
                        ),
                        mo.md(f"**Run summary:** {run_result.summary}"),
                        _comparison,
                        _stats,
                    ],
                    accent="#0f766e",
                    background="#f0fdfa",
                ),
                panel(
                    [
                        mo.md(
                            "### 3 · Follow the trajectory\n"
                            "Read downward. Each card separates the agent's proposal from what the environment actually allowed or returned."
                        ),
                        _trace,
                    ],
                    accent="#2563eb",
                ),
                panel(
                    [
                        mo.md(
                            "### 4 · Inspect the governed final state\n"
                            "This is the environment after the trajectory—not merely the model's last sentence."
                        ),
                        state_card(run_result.final_state),
                    ],
                    accent="#047857",
                    background="#f0fdf4",
                ),
                _warnings,
                _technical,
                panel(
                    [
                        mo.md(
                            "### 5 · Judge and redesign\n"
                            "A technically completed run can still be clinically wrong, poorly scoped, or unsafe."
                        ),
                        judgment_selector,
                        reflection_input,
                        mo.callout(
                            "Workshop prompt: What should the environment enforce instead of merely asking the model to remember?",
                            kind="info",
                        ),
                    ],
                    accent="#7c3aed",
                    background="#faf5ff",
                ),
            ],
            gap=1,
        )
    exercise_view = panel(
        [
            mo.md(f"### Exercise\n{selected_demo.exercise}"),
            mo.md(
                "**Interpretation boundary:** A completed technical run does not establish clinical correctness, safety, generalizability, or readiness for patient care."
            ),
        ],
        accent="#475569",
        background="#f8fafc",
    )
    result_section = mo.vstack([observed_view, exercise_view], gap=1)
    return result_section


@app.cell
def _(
    home_view,
    intro_view,
    mo,
    navigation_panel,
    navigation_toggle,
    result_section,
    selected_id,
):
    _global_styles = mo.Html(
        """
        <style>
          :root { --lab-ink: #0f172a; --lab-muted: #64748b; }
          body { background: #f1f5f9; }
          h1, h2, h3 { color: var(--lab-ink); letter-spacing: -0.02em; }
          p, li { line-height: 1.62; }
          pre { overflow-x: auto; }
          details summary::marker { color: #2563eb; }
        </style>
        """
    )
    _top_bar = mo.hstack(
        [
            navigation_toggle,
            mo.Html(
                '<div style="color:#f8fafc;font-weight:650;letter-spacing:.01em">'
                'Synthetic clinical simulation&nbsp;&nbsp;·&nbsp;&nbsp;'
                '<span style="color:#cbd5e1;font-weight:500">Follow the decision loop, not just the answer</span>'
                "</div>"
            ),
        ],
        justify="space-between",
        align="center",
        gap=1,
        wrap=True,
    ).style(
        {
            "background": "#0f172a",
            "color": "#f8fafc",
            "border-radius": "14px",
            "padding": ".7rem 1rem",
            "margin-bottom": "1rem",
            "box-shadow": "0 8px 24px rgba(15,23,42,.14)",
            "position": "sticky",
            "top": ".5rem",
            "z-index": "20",
        }
    )
    _visible_content = (
        [home_view] if selected_id is None else [intro_view, result_section]
    )
    _main_content = mo.vstack(_visible_content, gap=1).style(
        {"min-width": "0"}
    )
    if navigation_toggle.value:
        _body = mo.hstack(
            [navigation_panel, _main_content],
            widths=[0.27, 0.73],
            align="start",
            gap=1.2,
        )
    else:
        _body = _main_content
    mo.vstack([_global_styles, _top_bar, _body], gap=0).style(
        {"max-width": "1440px", "margin": "0 auto", "padding": ".75rem"}
    )
    return


if __name__ == "__main__":
    app.run()
