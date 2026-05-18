from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from .schemas import Resume


class ResumeParserState(BaseModel):
    resume_text: str
    parsed_resume: Resume | None = None
    error: str | None = None


def parse_resume(state: ResumeParserState) -> dict:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert resume parser. Extract structured information matching the schema precisely.",
            ),
            ("user", "Resume:\n\n{resume_text}"),
        ]
    )

    chain = prompt | structured_llm
    try:
        result = chain.invoke({"resume_text": state.resume_text})
        return {"parsed_resume": result}
    except Exception as e:
        return {"error": str(e)}


llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0,
)

structured_llm = llm.with_structured_output(Resume)

graph = StateGraph(ResumeParserState)

graph.add_node("parse_resume", parse_resume)

graph.add_edge(START, "parse_resume")
graph.add_edge("parse_resume", END)

compiled_graph = graph.compile()
