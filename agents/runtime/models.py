from dataclasses import dataclass, field
from typing import List


@dataclass
class TaskIntake:
    request_id: str
    date: str
    requested_by: str
    agent: str
    priority: str
    goal: str
    context: str
    constraints: str
    structured_data: str
    unstructured_notes: str
    output_format: str
    contains_health_data: bool
    external_communication: bool
    needs_supervisor_approval: bool


@dataclass
class AgentResponse:
    agent_name: str
    summary: str
    questions: List[str] = field(default_factory=list)
    action_plan: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [
            f"# {self.agent_name} Response",
            "",
            "## Summary",
            self.summary,
            "",
        ]

        if self.questions:
            lines.extend(["## Clarifying Questions"] + [f"- {q}" for q in self.questions] + [""])

        if self.action_plan:
            lines.extend(["## Action Plan"] + [f"- {item}" for item in self.action_plan] + [""])

        if self.risks:
            lines.extend(["## Risks & Guardrails"] + [f"- {r}" for r in self.risks] + [""])

        return "\n".join(lines).strip() + "\n"
