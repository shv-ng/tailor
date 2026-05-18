import operator
from typing import Annotated

from agents.gap_analyzer.runner import run_gap_analyzer
from agents.gap_analyzer.schemas import Gap
from agents.jd_analyzer.runner import run_jd_analyzer
from agents.jd_analyzer.schemas import Job
from agents.message_generator.runner import run_message_generator
from agents.message_generator.schemas import EmailStructure
from agents.question_generator.runner import run_question_generator
from agents.question_generator.schemas import Question
from agents.resume_parser.runner import run_resume_parser
from agents.resume_parser.schemas import Resume
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel
from apps.jobs.models import AgentResult


class SupervisorState(BaseModel):
    user_id: int | None = None
    resume_text: str | None = None
    jd_text: str | None = None
    parsed_resume: Resume | None = None
    parsed_jd: Job | None = None
    gap_analysis: Gap | None = None
    questions: list[Question] | None = None
    hr_email: EmailStructure | None = None
    referral_email: EmailStructure | None = None
    error: Annotated[list[str], operator.add] = []


def node_parse_resume(state: SupervisorState):
    if state.user_id:
        existing = AgentResult.objects.filter(
            user_id=state.user_id, agent_name="resume_parser"
        ).order_by('-created_at').first()

        if existing:
            return {"parsed_resume": Resume(**existing.result)}

    if not state.resume_text:
        return {"error": ["No resume text provided"]}
    try:
        res = run_resume_parser(state.resume_text)
        return {"parsed_resume": res.parsed_resume}
    except Exception as e:
        return {"error": [f"Error parsing resume: {str(e)}"]}


def node_analyze_jd(state: SupervisorState):
    if not state.jd_text:
        return {"error": ["No JD text provided"]}
    try:
        res = run_jd_analyzer(state.jd_text)
        return {"parsed_jd": res.parsed_jd}
    except Exception as e:
        return {"error": [f"Error analyzing JD: {str(e)}"]}


def node_analyze_gaps(state: SupervisorState):
    if not state.parsed_resume:
        return {"error": ["No parsed resume provided"]}
    if not state.parsed_jd:
        return {"error": ["No parsed JD provided"]}
    try:
        res = run_gap_analyzer(state.parsed_resume, state.parsed_jd)
        return {"gap_analysis": res.gap_analysis}
    except Exception as e:
        return {"error": [f"Error analyzing gaps: {str(e)}"]}


def node_generate_questions(state: SupervisorState):
    if not state.parsed_resume:
        return {"error": ["No parsed resume provided"]}
    if not state.parsed_jd:
        return {"error": ["No parsed JD provided"]}
    try:
        res = run_question_generator(state.parsed_resume, state.parsed_jd)
        return {"questions": res.questions}
    except Exception as e:
        return {"error": [f"Error generating questions: {str(e)}"]}


def node_generate_email(state: SupervisorState):
    if not state.parsed_resume:
        return {"error": ["No parsed resume provided"]}
    if not state.parsed_jd:
        return {"error": ["No parsed JD provided"]}
    try:
        res = run_message_generator(state.parsed_resume, state.parsed_jd)
        return {"hr_email": res.hr_email, "referral_email": res.referral_email}
    except Exception as e:
        return {"error": [f"Error generating email: {str(e)}"]}


llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.4,
)

graph = StateGraph(SupervisorState)

graph.add_node("node_parse_resume", node_parse_resume)
graph.add_node("node_analyze_jd", node_analyze_jd)
graph.add_node("node_analyze_gaps", node_analyze_gaps)
graph.add_node("node_generate_questions", node_generate_questions)
graph.add_node("node_generate_email", node_generate_email)

graph.add_edge(START, "node_parse_resume")
graph.add_edge(START, "node_analyze_jd")

graph.add_edge("node_parse_resume", "node_analyze_gaps")
graph.add_edge("node_analyze_jd", "node_analyze_gaps")

graph.add_edge("node_parse_resume", "node_generate_questions")
graph.add_edge("node_analyze_jd", "node_generate_questions")

graph.add_edge("node_parse_resume", "node_generate_email")
graph.add_edge("node_analyze_jd", "node_generate_email")

graph.add_edge("node_analyze_gaps", END)
graph.add_edge("node_generate_questions", END)
graph.add_edge("node_generate_email", END)

compiled_graph = graph.compile()
