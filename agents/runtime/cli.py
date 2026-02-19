import argparse
import json
from pathlib import Path

from .implementations import AGENT_REGISTRY
from .models import TaskIntake


def _load_intake(path: Path) -> TaskIntake:
    payload = json.loads(path.read_text())
    return TaskIntake(**payload)


def _run_single(agent_key: str, intake: TaskIntake) -> str:
    agent = AGENT_REGISTRY[agent_key]()
    return agent.run(intake).to_markdown()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Maharishi mission agents")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--agent", choices=AGENT_REGISTRY.keys(), help="Run one agent")
    mode.add_argument("--all", action="store_true", help="Run all agents")
    parser.add_argument("--input", required=True, help="Path to intake JSON")
    parser.add_argument("--output", required=False, help="Path to write markdown output")
    args = parser.parse_args()

    intake = _load_intake(Path(args.input))

    if args.all:
        sections = []
        for key in AGENT_REGISTRY:
            sections.append(_run_single(key, intake))
        markdown = "\n\n---\n\n".join(sections) + "\n"
    else:
        markdown = _run_single(args.agent, intake)

    if args.output:
        Path(args.output).write_text(markdown)
    else:
        print(markdown)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
