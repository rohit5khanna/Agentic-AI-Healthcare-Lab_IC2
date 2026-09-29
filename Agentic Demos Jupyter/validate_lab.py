"""Validate and execute every generated notebook in offline mock mode.

The validator intentionally avoids Jupyter/nbclient dependencies. The curriculum's
code cells are ordinary Python, so executing them sequentially provides a fast,
network-free preflight check. It does not persist cell outputs into the notebooks.
"""

from __future__ import annotations

import builtins
import contextlib
import io
import json
import os
import traceback
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NOTEBOOKS = ROOT
ARTIFACTS = ROOT / "artifacts"
REQUIRED_MARKERS = [
    "Learning objectives",
    "## Exercise",
    "Optional technical extension",
    "Interpretation boundary",
    "Exit question",
]


def text(cell: dict) -> str:
    source = cell.get("source", [])
    return source if isinstance(source, str) else "".join(source)


@contextlib.contextmanager
def offline_environment():
    keys = ["OPENAI_API_KEY", "OPENAI_BASE_URL", "MODEL", "FHIR_BASE_URL", "GATE_AUTO", "LAB_MODE"]
    previous = {key: os.environ.get(key) for key in keys}
    previous_backend = os.environ.get("MPLBACKEND")
    previous_input = builtins.input
    try:
        for key in keys:
            os.environ.pop(key, None)
        os.environ["LAB_MODE"] = "mock"
        os.environ["MPLBACKEND"] = "Agg"
        builtins.input = lambda *_args, **_kwargs: ""
        yield
    finally:
        builtins.input = previous_input
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        if previous_backend is None:
            os.environ.pop("MPLBACKEND", None)
        else:
            os.environ["MPLBACKEND"] = previous_backend


def validate_notebook(path: Path) -> dict:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook.get("cells", [])
    all_markdown = "\n".join(text(cell) for cell in cells if cell.get("cell_type") == "markdown")
    missing_markers = [marker for marker in REQUIRED_MARKERS if marker not in all_markdown]
    namespace = {"__name__": f"learning_lab_{path.stem}"}
    output = io.StringIO()
    errors = []
    executed = 0
    with offline_environment(), contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
        for index, cell in enumerate(cells, start=1):
            if cell.get("cell_type") != "code":
                continue
            source = text(cell)
            try:
                exec(compile(source, f"{path.name}:cell-{index}", "exec"), namespace)
                executed += 1
            except Exception as exc:  # noqa: BLE001 - validation must report every failure
                errors.append(
                    {
                        "cell": index,
                        "error": f"{type(exc).__name__}: {exc}",
                        "traceback": traceback.format_exc(limit=5),
                    }
                )
                break
    captured = output.getvalue()
    mode_ok = (
        "Backend: MOCK" in captured
        or path.name.startswith("05_")
        or path.name.startswith("07_")
    )
    return {
        "file": path.name,
        "cells": len(cells),
        "code_cells_executed": executed,
        "missing_required_sections": missing_markers,
        "mock_mode_confirmed": mode_ok,
        "errors": errors,
        "passed": not errors and not missing_markers and mode_ok,
        "output_tail": captured[-1500:],
    }


def render_markdown(results: list[dict]) -> str:
    passed = sum(result["passed"] for result in results)
    lines = [
        "# Jupyter learning lab validation",
        "",
        f"- Validated at: {datetime.now(timezone.utc).isoformat()}",
        f"- Notebooks passed: {passed}/{len(results)}",
        "- Execution mode: offline mock/deterministic",
        "- API credentials removed during validation: yes",
        "",
        "| Notebook | Cells | Code cells executed | Mock confirmed | Result |",
        "|---|---:|---:|---:|---|",
    ]
    for result in results:
        lines.append(
            f"| {result['file']} | {result['cells']} | {result['code_cells_executed']} | "
            f"{'yes' if result['mock_mode_confirmed'] else 'no'} | "
            f"{'PASS' if result['passed'] else 'FAIL'} |"
        )
    failures = [result for result in results if not result["passed"]]
    if failures:
        lines.extend(["", "## Failures", ""])
        for result in failures:
            lines.append(f"### {result['file']}")
            if result["missing_required_sections"]:
                lines.append(f"Missing sections: {result['missing_required_sections']}")
            for error in result["errors"]:
                lines.append(f"- Cell {error['cell']}: `{error['error']}`")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "A passing result confirms that notebook JSON is readable, required teaching sections are present, and code cells execute sequentially without an API key. It does not validate clinical correctness or live-model behavior.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    paths = sorted(NOTEBOOKS.glob("*.ipynb"))
    if len(paths) != 10:
        raise SystemExit(f"Expected 10 notebooks, found {len(paths)}. Check the repository contents.")
    results = [validate_notebook(path) for path in paths]
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    payload = {
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "offline_mock",
        "results": results,
    }
    (ARTIFACTS / "validation_results.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    (ARTIFACTS / "validation_report.md").write_text(render_markdown(results), encoding="utf-8")
    for result in results:
        print(f"{'PASS' if result['passed'] else 'FAIL'} {result['file']}")
        for error in result["errors"]:
            print(f"  cell {error['cell']}: {error['error']}")
    passed = sum(result["passed"] for result in results)
    print(f"\n{passed}/{len(results)} notebooks passed offline validation")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
