from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from .schemas import Job


class JDAnalyzerState(BaseModel):
    jd_text: str
    parsed_jd: Job | None = None
    error: str | None = None


def analyze_jd(state: JDAnalyzerState):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert job analyzer. Extract structured information matching the schema precisely.",
            ),
            ("user", "Job Description:\n\n{jd_text}"),
        ]
    )

    chain = prompt | structured_llm
    try:
        result = chain.invoke({"jd_text": state.jd_text})
        return {"parsed_jd": result}
    except Exception as e:
        return {"error": str(e)}


llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0,
)

structured_llm = llm.with_structured_output(Job)

graph = StateGraph(JDAnalyzerState)

graph.add_node("analyze_jd", analyze_jd)

graph.add_edge(START, "analyze_jd")
graph.add_edge("analyze_jd", END)

compiled_graph = graph.compile()
