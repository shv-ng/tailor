from rest_framework import routers
from django.urls import path
from django.urls import include

from . import views

router = routers.DefaultRouter()
router.register("jobs", views.JobApplicationViewSet, basename="jobs")

urlpatterns = [
    path("jobs/analyze/", views.JobAnalyseView.as_view(), name="analyze"),
    path("", include(router.urls)),
]
