from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class JobApplication(models.Model):
    class JobStatus(models.TextChoices):
        APPLIED = "applied"
        INTERVIEWED = "interviewed"
        REJECTED = "rejected"
        OFFERED = "offered"
        PROCESSING = "processing"
        FAILED = "failed"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField()
    role = models.CharField()
    jd_text = models.TextField()
    jd_url = models.URLField(null=True, blank=True)
    status = models.CharField(choices=JobStatus.choices, default=JobStatus.PROCESSING)
    profile_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.role} - {self.company_name}"


class AgentResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(
        JobApplication, on_delete=models.CASCADE, null=True, blank=True
    )
    agent_name = models.CharField()
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.agent_name} - {self.application}"
