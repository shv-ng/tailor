import logging
import time

from .graph import SupervisorState, compiled_graph

logger = logging.getLogger(__name__)


def run_supervisor(resume_text: str, jd_text: str, user_id: int | None = None):
    initial_state = SupervisorState(
        resume_text=resume_text, jd_text=jd_text, user_id=user_id
    )
    final_state = compiled_graph.invoke(initial_state)

    if final_state.get("error"):
        for err in final_state["error"]:
            logger.error(err)
    return SupervisorState(**final_state)


if __name__ == "__main__":
    # Test dataset configuration
    sample_resume_md = """
    # Shivang Srivastava
    Backend Engineer | Go, Python, Rust
    Email: shivangsrivastava157@gmail.com
    
    ## Projects
    ### Relay
    - Built a high-performance HTTP load balancer from scratch in Go.
    - Implemented 5 network traffic balancing routing algorithms.
    """

    sample_jd_raw = """
    🐋 Open Source Contributor — OrcaRouter
    Company: OrcaRouter (Remote)
    Looking for backend systems engineers with strong Go or Python skills to design 
    LLM routing models, prompt caching engines, and custom performance balancers.
    """

    print("🚀 Initiating Master Supervisor Orchestrator Agent...")
    start_time = time.time()

    output = run_supervisor(resume_text=sample_resume_md, jd_text=sample_jd_raw)

    end_time = time.time()
    execution_duration = end_time - start_time

    print("\n" + "=" * 20 + " PIPELINE EXECUTION SUCCESS " + "=" * 20)
    print(f"⏱️ Total Execution Time: {execution_duration:.2f} seconds\n")

    print("📊 Profile Gap Score:")
    if output.gap_analysis:
        print(f"-> {output.gap_analysis.profile_score}/100")

    print("\n📝 Interview Prep Samples (First 2):")
    if output.questions:
        for q in output.questions[:2]:
            print(f" - [{q.category}] {q.question}")

    print("\n📧 Generated Outreach Material:")
    if output.hr_email:
        print(f" -> Recruiter Email Subject: {output.hr_email.subject}")
    if output.referral_email:
        print(f" -> SDE Referral Subject: {output.referral_email.subject}")
    print("=" * 68)

    print(output)
