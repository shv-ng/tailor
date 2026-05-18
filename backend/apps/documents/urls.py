from django.urls import path

from .views import CurrentResumeView, ResumeUploadView

urlpatterns = [
    path("resumes/upload/", ResumeUploadView.as_view(), name="resume-upload"),
    path("resumes/me/", CurrentResumeView.as_view(), name="current-resume"),
]
