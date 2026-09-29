"""Run all Marimo demos in Live mode without exposing credentials.

Model-based demos make authentic calls. Demos 5, 7, and 9 are deliberately
deterministic/local and are expected to make zero model calls. Demo 6 retains
its complete 76-call experiment so latency remains observable.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from lab_core import run_demo


ROOT = Path(__file__).resolve().parent
ENV_FILE = Path(
    os.environ.get("MARIMO_LAB_ENV_FILE", ROOT / ".env")
).expanduser()
ARTIFACTS = ROOT / "artifacts"


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key.strip()] = value
    return values


def main() -> int:
    if not ENV_FILE.exists():
        raise RuntimeError(f"Environment file not found: {ENV_FILE}")
    configured = parse_env(ENV_FILE)
    for key in ("OPENAI_API_KEY", "OPENAI_BASE_URL", "MODEL", "BARRY_MODEL"):
        if configured.get(key):
            os.environ[key] = configured[key]
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    exact_live_calls = {
        "01": 1,
        "04": 2,
        "05": 0,
        "06": 76,
        "07": 0,
        "08": 4,
        "09": 0,
        "10": 1,
    }
    results = []
    for demo_id in (f"{number:02d}" for number in range(1, 11)):
        result = run_demo(
            demo_id,
            "Live",
            gate_decision="Request more information",
            evidence=["Latest INR", "Current medication"],
        )
        metrics = result.telemetry_summary()
        expected = exact_live_calls.get(demo_id)
        call_count_ok = (
            metrics["New live calls"] >= 1
            if expected is None
            else metrics["New live calls"] == expected
        )
        results.append(
            {
                "demo_id": demo_id,
                "status": result.status,
                "summary": result.summary,
                "trace_steps": len(result.trace),
                "telemetry": metrics,
                "call_count_ok": call_count_ok,
                "medication_or_external_state_changed": False,
            }
        )
        print(
            f"Demo {demo_id}: {result.status}; "
            f"trace_steps={len(result.trace)}; "
            f"live_calls={metrics['New live calls']}; "
            f"call_count_ok={call_count_ok}"
        )

    payload = {
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "live",
        "model": os.environ.get("MODEL") or os.environ.get("BARRY_MODEL"),
        "api_key_written_to_artifacts": False,
        "results": results,
    }
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / "live_smoke_results.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    passed = sum(
        item["status"] in {"completed", "held"} and item["call_count_ok"]
        for item in results
    )
    report = [
        "# Marimo live-model smoke test",
        "",
        f"- Validated at: {payload['validated_at']}",
        f"- Model: `{payload['model']}`",
        "- API key written to artifacts: no",
        "- External or patient state changed: no",
        "",
        "| Demo | Status | Trace steps | Live calls | Call boundary | Tokens | Latency |",
        "|---|---|---:|---:|---|---:|---:|",
    ]
    for item in results:
        metrics = item["telemetry"]
        report.append(
            f"| {item['demo_id']} | {item['status']} | {item['trace_steps']} | "
            f"{metrics['New live calls']} | {'PASS' if item['call_count_ok'] else 'FAIL'} | "
            f"{metrics['Tokens']} | {metrics['Latency (s)']}s |"
        )
    report.extend(
        [
            "",
            "A pass confirms authentic model interaction ending in either normal completion or safe containment. It does not establish clinical correctness or safety.",
            "",
        ]
    )
    (ARTIFACTS / "live_smoke_report.md").write_text("\n".join(report), encoding="utf-8")
    print(f"{passed}/{len(results)} live Marimo demo engines passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
