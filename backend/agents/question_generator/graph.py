from agents.jd_analyzer.schemas import Job
from agents.resume_parser.graph import Resume
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from .schemas import InterviewPrep, Question


class QuestionGeneratorState(BaseModel):
    parsed_resume: Resume | None = None
    parsed_jd: Job | None = None
    questions: list[Question] | None = None
    error: str | None = None


def generate_questions(state: QuestionGeneratorState):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an elite, highly technical hiring architect generating hyper-tailored interview preparation material.
            Your goal is to inspect a candidate's resume alongside a Job Description (JD) and build exactly 5 highly customized interview questions.
            
            CRITICAL RULES:
            - Generate EXACTLY 5 questions spanning categories: technical, behavioral, project-based, role-specific.
            - Ground your questions and answers explicitly in the candidate's actual history.
            - If it's a project-based or technical question, explicitly target their exact projects by name and their actual backend stack.
            - The 'answer' must demonstrate how THIS specific candidate should respond leveraging their real technical background. No generic templates allowed.""",
            ),
            (
                "user",
                """Generate 5 tailored prep questions for this candidate mapping to this role:
            
            ### CANDIDATE RESUME:
            {resume_data}
            
            ### TARGET JOB DESCRIPTION:
            {jd_data}
            
            Extract structured data exactly matching the requested structured schema.""",
            ),
        ]
    )

    chain = prompt | structured_llm
    try:
        resume_str = (
            state.parsed_resume.model_dump_json(indent=2)
            if state.parsed_resume
            else "None"
        )
        jd_str = (
            state.parsed_jd.model_dump_json(indent=2) if state.parsed_jd else "None"
        )

        result = chain.invoke({"resume_data": resume_str, "jd_data": jd_str})
        return {"questions": result.questions, "error": None}
    except Exception as e:
        return {"error": str(e)}


llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.3,
)

structured_llm = llm.with_structured_output(InterviewPrep)

graph = StateGraph(QuestionGeneratorState)

graph.add_node("generate_questions", generate_questions)

graph.add_edge(START, "generate_questions")
graph.add_edge("generate_questions", END)

compiled_graph = graph.compile()
