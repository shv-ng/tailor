from rest_framework import serializers

from .models import Resume


class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "file", "original_filename", "uploaded_at"]
        read_only_fields = ["id", "original_filename", "uploaded_at"]

    def validate_file(self, value):
        if value.content_type != "application/pdf" and not value.name.endswith(".pdf"):
            raise serializers.ValidationError("Only PDF files are allowed")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        try:
            file = validated_data["file"]
        except KeyError:
            raise serializers.ValidationError("File is required")

        Resume.objects.filter(user=user, is_active=True).update(is_active=False)

        return Resume.objects.create(
            user=user,
            file=file,
            original_filename=file.name,
            is_active=True,
        )


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "original_filename", "uploaded_at", "is_active"]
