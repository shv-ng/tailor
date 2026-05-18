from django.contrib import admin

from .models import AgentResult, JobApplication

admin.site.register(JobApplication)
admin.site.register(AgentResult)
