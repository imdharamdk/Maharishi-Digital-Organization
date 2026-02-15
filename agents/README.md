# AI Agent Starter Pack

This folder now contains both:
1. Agent design specs (`*.md`)
2. Runnable Python implementations (`runtime/`)

## Included mission agents
1. Ayurveda Knowledge Agent
2. Yoga Program Agent
3. Healthcare Outreach Agent
4. Education Agent
5. Operations Agent

## Quick start (programmed agents)
1. Prepare an intake JSON (example: `sample-intake.json`).
2. Run an agent:
   ```bash
   python -m agents.runtime.cli --agent operations --input agents/sample-intake.json
   ```
3. Run all agents at once (execute mode):
   ```bash
   python -m agents.runtime.cli --all --input agents/sample-intake.json --output /tmp/all-agents.md
   ```
4. Optional: run one agent and save output to file:
   ```bash
   python -m agents.runtime.cli --agent education --input agents/sample-intake.json --output /tmp/education.md
   ```

## Agent keys for CLI
- `operations`
- `ayurveda`
- `yoga`
- `healthcare`
- `education`

## Shared guardrails (apply to all agents)
- Never provide medical diagnosis or emergency advice.
- Ask for missing context before final recommendations.
- Mark uncertainty explicitly.
- Require human approval for external communication, financial decisions, and health-related recommendations.
- Keep personal data minimal and masked where possible.

## Testing
Run unit tests:
```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```
