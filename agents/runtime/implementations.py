from .base import BaseAgent
from .models import TaskIntake, AgentResponse


class OperationsAgent(BaseAgent):
    name = "Operations Agent"

    def _build_response(self, intake: TaskIntake) -> AgentResponse:
        questions = []
        if "owner" not in intake.structured_data.lower():
            questions.append("Please provide task owners for all deliverables.")
        if "due" not in intake.structured_data.lower():
            questions.append("Please provide due dates for each task.")

        return AgentResponse(
            agent_name=self.name,
            summary="Converted operational context into a prioritized execution checklist.",
            questions=questions,
            action_plan=[
                "Extract action items from notes and map each item to owner + due date.",
                "Prioritize tasks into High / Medium / Low urgency buckets.",
                "Publish daily status with blockers and escalation owner.",
            ],
        )


class AyurvedaKnowledgeAgent(BaseAgent):
    name = "Ayurveda Knowledge Agent"

    def _build_response(self, intake: TaskIntake) -> AgentResponse:
        return AgentResponse(
            agent_name=self.name,
            summary="Prepared education-first Ayurveda content plan grounded in approved sources.",
            action_plan=[
                "List approved references and map claims to each source.",
                "Create beginner summary with Hindi + English terminology.",
                "Add disclaimer: educational content only, not medical diagnosis.",
            ],
            risks=["Do not publish content that lacks approved source mapping."],
        )


class YogaProgramAgent(BaseAgent):
    name = "Yoga Program Agent"

    def _build_response(self, intake: TaskIntake) -> AgentResponse:
        return AgentResponse(
            agent_name=self.name,
            summary="Generated a goal-based yoga session framework with safety constraints.",
            action_plan=[
                "Build session blocks: warm-up, main sequence, cool-down.",
                "Annotate contraindications and safer alternatives.",
                "Create weekly progression with instructor check-in points.",
            ],
            risks=["Avoid treatment claims; route medical concerns to professionals."],
        )


class HealthcareOutreachAgent(BaseAgent):
    name = "Healthcare Outreach Agent"

    def _build_response(self, intake: TaskIntake) -> AgentResponse:
        return AgentResponse(
            agent_name=self.name,
            summary="Built outreach operations checklist for pre-camp and post-camp execution.",
            action_plan=[
                "Create volunteer roster by shift and responsibility.",
                "Generate camp-day checklist (registration, triage, flow, closure).",
                "Track follow-ups at 7-day and 30-day intervals.",
            ],
            risks=["Any clinical recommendation must be reviewed by a qualified supervisor."],
        )


class EducationAgent(BaseAgent):
    name = "Education Agent"

    def _build_response(self, intake: TaskIntake) -> AgentResponse:
        return AgentResponse(
            agent_name=self.name,
            summary="Designed inclusive, multilingual lesson planning flow with measurable outcomes.",
            action_plan=[
                "Define weekly learning objectives by learner level.",
                "Draft low-resource activities and worksheet prompts.",
                "Attach rubric for attendance, completion, and assessment score.",
            ],
        )


AGENT_REGISTRY = {
    "operations": OperationsAgent,
    "ayurveda": AyurvedaKnowledgeAgent,
    "yoga": YogaProgramAgent,
    "healthcare": HealthcareOutreachAgent,
    "education": EducationAgent,
}
