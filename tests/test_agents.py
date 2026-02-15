import subprocess
import tempfile
import unittest
from pathlib import Path

from agents.runtime.implementations import AGENT_REGISTRY
from agents.runtime.models import TaskIntake


class AgentRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.intake = TaskIntake(
            request_id="REQ-TEST",
            date="2026-02-15",
            requested_by="Tester",
            agent="operations",
            priority="High",
            goal="Test",
            context="Ctx",
            constraints="None",
            structured_data="Task: X; Owner: Y; Due: Tomorrow",
            unstructured_notes="Notes",
            output_format="table",
            contains_health_data=False,
            external_communication=True,
            needs_supervisor_approval=True,
        )

    def test_registry_contains_all_agents(self):
        self.assertEqual(
            set(AGENT_REGISTRY.keys()),
            {"operations", "ayurveda", "yoga", "healthcare", "education"},
        )

    def test_all_agents_generate_markdown(self):
        for key, cls in AGENT_REGISTRY.items():
            self.intake.agent = key
            response = cls().run(self.intake)
            markdown = response.to_markdown()
            self.assertIn("## Summary", markdown)
            self.assertIn("## Action Plan", markdown)

    def test_guardrails_added(self):
        response = AGENT_REGISTRY["operations"]().run(self.intake)
        text = " ".join(response.risks)
        self.assertIn("External communication", text)
        self.assertIn("Supervisor approval", text)

    def test_cli_all_executes_every_agent(self):
        with tempfile.NamedTemporaryFile(suffix=".md") as out:
            subprocess.run(
                [
                    "python",
                    "-m",
                    "agents.runtime.cli",
                    "--all",
                    "--input",
                    "agents/sample-intake.json",
                    "--output",
                    out.name,
                ],
                check=True,
            )
            content = Path(out.name).read_text()
            for expected in [
                "# Operations Agent Response",
                "# Ayurveda Knowledge Agent Response",
                "# Yoga Program Agent Response",
                "# Healthcare Outreach Agent Response",
                "# Education Agent Response",
            ]:
                self.assertIn(expected, content)


if __name__ == "__main__":
    unittest.main()
