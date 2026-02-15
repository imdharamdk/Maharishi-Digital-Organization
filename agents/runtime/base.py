from abc import ABC, abstractmethod
from .models import TaskIntake, AgentResponse


class BaseAgent(ABC):
    name: str = "BaseAgent"

    def run(self, intake: TaskIntake) -> AgentResponse:
        response = self._build_response(intake)
        response.risks.extend(self._default_guardrails(intake))
        return response

    @abstractmethod
    def _build_response(self, intake: TaskIntake) -> AgentResponse:
        raise NotImplementedError

    def _default_guardrails(self, intake: TaskIntake) -> list[str]:
        risks: list[str] = []
        if intake.contains_health_data:
            risks.append("Contains health data: mask personal identifiers and restrict sharing.")
        if intake.external_communication:
            risks.append("External communication required: obtain human approval before sending.")
        if intake.needs_supervisor_approval:
            risks.append("Supervisor approval required before execution.")
        return risks
