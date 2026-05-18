from agents.jd_analyzer.schemas import Job
from agents.resume_parser.graph import Resume
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from .schemas import Gap


class GapAnalyzerState(BaseModel):
    parsed_resume: Resume | None = None
    parsed_jd: Job | None = None
    gap_analysis: Gap | None = None
    error: str | None = None


def analyze_gap(state: GapAnalyzerState):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an elite, brutally honest technical recruiter and gap analyzer. 
            Your task is to compare a candidate's parsed resume against a parsed job description (JD).
            
            CRITICAL CRITERIA:
            - Be highly strict and objective. Do NOT be generous or give the benefit of the doubt.
            - A perfect score of 90-100 should be exceptionally rare and reserved for exact matching profiles.
            - Focus heavily on missing core infrastructure tools, systems programming skills, and algorithmic requirements.""",
            ),
            (
                "user",
                """Compare the following Resume and Job Description:
            
            ### PARSED RESUME:
            {resume_data}
            
            ### PARSED JOB DESCRIPTION:
            {jd_data}
            
            Extract structured data exactly matching the requested schema output.""",
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
        return {"gap_analysis": result}
    except Exception as e:
        return {"error": str(e)}


llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0,
)

structured_llm = llm.with_structured_output(Gap)

graph = StateGraph(GapAnalyzerState)

graph.add_node("analyze_gap", analyze_gap)

graph.add_edge(START, "analyze_gap")
graph.add_edge("analyze_gap", END)

compiled_graph = graph.compile()
