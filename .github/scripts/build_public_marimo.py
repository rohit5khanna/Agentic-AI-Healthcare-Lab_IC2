"""Build a self-contained, browser-safe Marimo notebook for GitHub Pages.

The canonical application keeps its testable engine in ``lab_core.py``. A
WebAssembly export cannot rely on that adjacent module, so this build step
embeds it in a temporary generated notebook. It also removes Live mode from
the public selector: browser visitors can use Explore and Replay without ever
being asked for an API credential.
"""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APP_DIR = ROOT / "Agentic Learning Lab Marimo"
APP_PATH = APP_DIR / "healthcare_agent_learning_lab.py"
CORE_PATH = APP_DIR / "lab_core.py"


def replace_once(source: str, old: str, new: str, label: str) -> str:
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one {label} marker, found {count}.")
    return source.replace(old, new, 1)


def build(output: Path) -> Path:
    app_source = APP_PATH.read_text(encoding="utf-8")
    core_source = CORE_PATH.read_text(encoding="utf-8")

    embedded_core = (
        "    import sys as _sys\n"
        "    import types as _types\n\n"
        "    _lab_core = _types.ModuleType(\"lab_core\")\n"
        "    _sys.modules[\"lab_core\"] = _lab_core\n"
        f"    exec(compile({core_source!r}, \"lab_core.py\", \"exec\"), _lab_core.__dict__)\n"
        "    CASE_CARDS = _lab_core.CASE_CARDS\n"
        "    CATALOG_BY_ID = _lab_core.CATALOG_BY_ID\n"
        "    DEMO_CATALOG = _lab_core.DEMO_CATALOG\n"
        "    run_demo = _lab_core.run_demo"
    )
    app_source = replace_once(
        app_source,
        "    from lab_core import CASE_CARDS, CATALOG_BY_ID, DEMO_CATALOG, run_demo",
        embedded_core,
        "lab_core import",
    )
    app_source = replace_once(
        app_source,
        '        options=["Explore", "Replay", "Live"],',
        '        options=["Explore", "Replay"],',
        "execution-mode selector",
    )
    app_source = replace_once(
        app_source,
        '                    mo.stat("3", label="Execution modes", bordered=True),',
        '                    mo.stat("2", label="Public execution modes", bordered=True),',
        "execution-mode statistic",
    )
    app_source = replace_once(
        app_source,
        '                "Live = authentic model response"',
        '                "Live = available only in the facilitator-hosted edition"',
        "mode guide",
    )
    app_source = replace_once(
        app_source,
        '                                "### Live\\n"\n'
        '                                "Authentic model behavior with visible latency, token use, and safe containment of malformed or unexpected proposals."',
        '                                "### Live (facilitator-hosted)\\n"\n'
        '                                "Not available in this public browser edition. This keeps API credentials off participant devices."',
        "Home Live card",
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(app_source, encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / ".pages" / "healthcare_agent_learning_lab_public.py",
    )
    args = parser.parse_args()
    result = build(args.output.resolve())
    print(result)


if __name__ == "__main__":
    main()
