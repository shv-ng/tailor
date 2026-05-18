from agents.jd_analyzer.schemas import Job
from agents.resume_parser.graph import Resume
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from .schemas import EmailStructure


class MessageGeneratorState(BaseModel):
    parsed_resume: Resume | None = None
    parsed_jd: Job | None = None
    hr_email: EmailStructure | None = None
    referral_email: EmailStructure | None = None
    error: str | None = None


def generate_hr_email(state: MessageGeneratorState):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are the candidate writing a hyper-targeted cold outreach email 
to an HR recruiter. Your goal is a human-sounding email that gets 
a reply, NOT a cover letter.

RULES — follow every one, no exceptions:

HOOK (1-2 sentences):
- Open with ONE specific, verifiable detail about the company pulled 
  from the JD — a technology choice they made, a product they 
  recently built, a specific engineering challenge they mentioned, 
  or a company milestone. Do NOT write "I've been following your 
  work" or "I am impressed by." Write something a generic 
  applicant could NOT have written.

PROOF (2-3 sentences, NO bullets):
- State ONE specific project or result that directly mirrors the 
  company's problem. Include a concrete metric (e.g. "reduced p99 
  latency from 340ms to 90ms", "handled 500 RPS under load"). 
  If the resume lacks explicit numbers, derive a plausible 
  relative metric ("~3x throughput improvement"). 
  Name the exact tech that matches the JD.

ASK (1 sentence):
- End with: "Open to a 10-minute call?" — nothing more.

SUBJECT LINE:
- Casual, specific, under 8 words. Reference something real from 
  the JD (a tech, a product, a problem). 
  NOT "Candidate: [Role] | [USP]" — that looks like a template.

ABSOLUTE BANS:
- No bullets or numbered lists anywhere
- No "I am passionate about"
- No "aligns perfectly with your mission"  
- No "I hope this finds you well"
- No "Here is why I am a strong fit"
- No "I know you are busy"
- Word count: under 100 words for the body (excluding subject)
- Tone: conversational, peer-level, zero corporate fluff""",
            ),
            (
                "user",
                "Resume:\n{resume}\n\nJD:\n{jd}\n\nGenerate the HR email structure:",
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

        result = chain.invoke({"resume": resume_str, "jd": jd_str})

        return {"hr_email": result}
    except Exception as e:
        return {"error": f"Error generating HR email: {str(e)}"}


def generate_referral_email(state: MessageGeneratorState):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """ You are the candidate writing a peer-to-peer cold email to a 
software engineer at the target company, asking for an internal 
referral. You are one engineer talking to another.

RULES — follow every one, no exceptions:

OPENER (1 sentence):
- Jump straight in. Reference ONE specific technical detail from 
  the JD — a stack choice, an architecture decision, a known 
  engineering challenge at this company. This proves you did 
  your homework. Do NOT start with "I know you are busy", 
  "I hope this finds you well", or any apology.

CONNECTION (2-3 sentences):
- In plain prose (NO bullets), state ONE concrete project 
  from your resume that is directly relevant to what their 
  team works on. Include a specific metric or technical outcome. 
  Be direct about the role you're targeting.

ASK (1 sentence):
- End with: "Would you be open to forwarding my resume?" 
  or "Happy to send my resume if you're open to passing it along."

SUBJECT LINE:
- Write like a peer, not a recruiter. Casual, specific, 
  under 7 words. Examples: "Backend eng interested in your 
  infra work", "Quick ask — [Company] referral"

ABSOLUTE BANS:
- No bullets or numbered lists
- No "I am very interested in"
- No "I believe my background aligns"
- No apology openers of any kind
- No "passionate", "aligns perfectly", "strong fit"
- Word count: under 90 words for body (excluding subject)
- Tone: direct, technical, peer-level — like a Slack DM, 
  not a cover letter
                """
            ),
            (
                "user",
                "Resume:\n{resume}\n\nJD:\n{jd}\n\nGenerate the engineering referral email structure:",
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

        result = chain.invoke({"resume": resume_str, "jd": jd_str})
        return {"referral_email": result}

    except Exception as e:
        return {"error": f"Error generating referral email: {str(e)}"}


llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.4,
)


graph = StateGraph(MessageGeneratorState)

structured_llm = llm.with_structured_output(EmailStructure)
graph.add_node("generate_hr_email", generate_hr_email)
graph.add_node("generate_referral_email", generate_referral_email)

graph.add_edge(START, "generate_hr_email")
graph.add_edge(START, "generate_referral_email")

graph.add_edge("generate_hr_email", END)
graph.add_edge("generate_referral_email", END)

compiled_graph = graph.compile()
