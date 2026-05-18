from celery import shared_task

from agents.supervisor.runner import run_supervisor
from apps.jobs.models import JobApplication, AgentResult
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def run_supervisor_task(
    self,
    *,
    job_application_id: int,
    resume_text: str,
    jd_text: str,
    user_id: int | None = None,
):
    try:
        job_application = JobApplication.objects.get(id=job_application_id)

        result = run_supervisor(resume_text, jd_text, user_id)

        gap_output = result.gap_analysis
        profile_score = gap_output.profile_score if gap_output else 0

        job_application.profile_score = profile_score
        job_application.company_name = (
            result.parsed_jd.company
            if result.parsed_jd
            else job_application.company_name
        )
        job_application.role = (
            result.parsed_jd.role if result.parsed_jd else job_application.role
        )
        job_application.status = JobApplication.JobStatus.APPLIED
        job_application.save(
            update_fields=["profile_score", "company_name", "role", "status"]
        )

        agent_mapping = {
            "resume_parser": result.parsed_resume.model_dump()
            if result.parsed_resume
            else {},
            "jd_analyzer": result.parsed_jd.model_dump() if result.parsed_jd else {},
            "gap_analyzer": gap_output.model_dump() if gap_output else {},
            "question_generator": [q.model_dump() for q in result.questions]
            if result.questions
            else [],
            "message_generator": {
                "hr_email": result.hr_email.model_dump() if result.hr_email else None,
                "referral_email": result.referral_email.model_dump()
                if result.referral_email
                else None,
            },
        }

        for agent_name, agent_output in agent_mapping.items():
            AgentResult.objects.create(
                user_id=user_id,
                application=job_application,
                agent_name=agent_name,
                result=agent_output,
            )
    except Exception as e:
        logger.error(
            f"analyse_job_task failed for job_application_id={job_application_id}: {e}"
        )
        try:
            JobApplication.objects.filter(id=job_application_id).update(
                status=JobApplication.JobStatus.FAILED
            )
        except Exception:
            pass
        raise self.retry(exc=e, countdown=10)
