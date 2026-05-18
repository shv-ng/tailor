from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from tasks.celery import run_supervisor_task
from rest_framework.decorators import action

from .models import JobApplication
from .serializers import (
    JobAnalyseSerializer,
    JobApplicationDetailSerializer,
    JobApplicationListSerializer,
)


class JobAnalyseView(APIView):
    def post(self, request):
        serializer = JobAnalyseSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        jd_text = serializer.data.get("jd_text")
        jd_url = serializer.data.get("jd_url")
        if not jd_text:
            return Response(
                {"detail": "Please provide jd_text in the request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        active_resume = request.user.resume_set.filter(is_active=True).first()

        if not active_resume:
            return Response(
                {
                    "detail": "No active resume found. Please upload and activate a resume first."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        resume_text = active_resume.extracted_text

        job_application = JobApplication.objects.create(
            user=request.user,
            company_name="",
            role="",
            jd_text=jd_text,
            jd_url=jd_url,
            status=JobApplication.JobStatus.PROCESSING,
        )

        run_supervisor_task.delay(
            job_application_id=job_application.id,
            resume_text=resume_text,
            jd_text=jd_text,
            user_id=request.user.id,
        )

        return Response(
            {
                "job_application_id": job_application.id,
                "status": job_application.status,
                "detail": "Job Application is being processed. Please check back later for the results.",
            },
            status=status.HTTP_201_CREATED,
        )


class JobApplicationViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user).order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "list":
            return JobApplicationListSerializer
        return JobApplicationDetailSerializer

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        print(request.data)
        job = self.get_object()

        new_status = request.data.get("status")
        if not new_status:
            return Response(
                {"detail": "status field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_statuses = [choice[0] for choice in JobApplication.JobStatus.choices]
        if new_status not in valid_statuses:
            return Response(
                {"detail": f"Invalid status. Allowed values: {valid_statuses}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        job.status = new_status
        job.save(update_fields=["status"])

        serializer = JobApplicationDetailSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)
