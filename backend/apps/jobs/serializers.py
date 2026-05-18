from collections import defaultdict

from rest_framework import serializers

from .models import AgentResult, JobApplication


class JobAnalyseSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["jd_text", "jd_url"]


class JobApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["id", "company_name", "role", "profile_score", "status", "created_at"]


class AgentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentResult
        fields = ["id", "agent_name", "result", "created_at"]


class JobApplicationDetailSerializer(serializers.ModelSerializer):
    agent_results = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = [
            "id",
            "company_name",
            "role",
            "jd_text",
            "jd_url",
            "profile_score",
            "status",
            "created_at",
            "agent_results",
        ]

    def get_agent_results(self, obj):
        results = obj.agentresult_set.all()

        grouped = defaultdict(list)
        for result in results:
            grouped[result.agent_name].append(
                {
                    "id": result.id,
                    "result": result.result,
                    "created_at": result.created_at,
                }
            )

        return grouped
