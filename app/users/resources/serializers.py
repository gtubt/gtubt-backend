from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DefaultRegisterSerializer,
)
from rest_framework import serializers

from app.users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=255, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "last_name",
            "department",
            "year",
            "student_id",
            "photo_url",
            "phone",
            "is_active",
            "password",
        ]


class RegisterSerializer(DefaultRegisterSerializer):
    username = serializers.CharField(max_length=255, default="", required=False)
