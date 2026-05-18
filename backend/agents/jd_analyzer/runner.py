import logging

from .graph import JDAnalyzerState, compiled_graph

logger = logging.getLogger(__name__)


def run_jd_analyzer(jd_text: str) -> JDAnalyzerState:
    initial_state = JDAnalyzerState(jd_text=jd_text)
    final_state = compiled_graph.invoke(initial_state)
    if final_state.get("error"):
        logger.error(final_state.get("error"))
    return JDAnalyzerState(**final_state)


if __name__ == "__main__":
    sample_jd = """

OrcaRouter logo
OrcaRouter
Share
Show more options
🐋 Open Source Contributor — OrcaRouter
India · 1 week ago · Over 100 applicants
Promoted by hirer · Actively reviewing applicants


Remote

Full-time

Easy Apply

Save
Save 🐋 Open Source Contributor — OrcaRouter at OrcaRouter
🐋 Open Source Contributor — OrcaRouter
OrcaRouter · India (Remote)

Easy Apply

Save
Save 🐋 Open Source Contributor — OrcaRouter at OrcaRouter
Show more options
How your profile and resume fit this job
Get AI-powered advice on this job and more exclusive features with Premium. Try Premium for ₹0



Show match details

Tailor my resume

Help me stand out

About the job
Build the routing layer for the AI internet.



OrcaRouter is an open, zero-markup LLM router that automatically matches every prompt to the best model — across OpenAI, Anthropic, Google, open-source, and more.



We’re building the control plane for AI inference: routing, caching, cost optimization, and eventually monetization (rewards, infra).


If you care about LLMs, systems, performance, or open infrastructure, this is for you.


What you will work on:

LLM Routing model (cost vs quality vs latency)
Adaptive routing (embeddings, bandits, heuristics, eval-driven)
Prompt Caching: Deterministic caching across providers
Cache invalidation, hashing, replay
Inference Optimization: Batching, KV-cache routing, streaming
Latency + throughput improvements
Provider Integrations: OpenAI, Anthropic, Gemini, Groq, open-source models
OpenAI-compatible API layer
Developer Experience: SDK improvements & Integrations
CLI, dashboards, local-first workflows
Future (if you’re cracked) Cost prediction engine
Reward modeling / routing feedback loops
Token-level monetization

    """

    print("⏳ Running JD Analyzer Agent...")
    result = run_jd_analyzer(sample_jd)

    import pprint

    pprint.pprint(result.parsed_jd)
