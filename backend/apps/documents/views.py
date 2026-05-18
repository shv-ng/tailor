from django.db import transaction
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Resume
from .serializers import ResumeSerializer, ResumeUploadSerializer
from .utils import extract_text_from_pdf
from agents.resume_parser.runner import run_resume_parser
from apps.jobs.models import AgentResult


class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = ResumeUploadSerializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                resume = serializer.save()

                extracted_text = extract_text_from_pdf(resume.file.path)
                resume.extracted_text = extracted_text
                resume.save(update_fields=["extracted_text"])

                parsed = run_resume_parser(extracted_text)
                AgentResult.objects.create(
                    user=request.user,
                    application=None,
                    agent_name="resume_parser",
                    result=parsed.parsed_resume.model_dump()
                    if parsed.parsed_resume
                    else {},
                )
        except Exception as e:
            if resume and resume.file:
                resume.file.delete(save=False)

            resume.delete()
            raise e

        return Response(
            {
                "id": resume.id,
                "filename": resume.original_filename,
                "uploaded_at": resume.uploaded_at,
            },
            status=status.HTTP_201_CREATED,
        )


class CurrentResumeView(APIView):
    def get(self, request):
        resume = Resume.objects.filter(user=request.user, is_active=True).first()
        if not resume:
            return Response(
                {"detail": "No active resume found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ResumeSerializer(resume)
        return Response(serializer.data, status=status.HTTP_200_OK)
