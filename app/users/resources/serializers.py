from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DefaultRegisterSerializer,
)
from rest_framework import serializers

from app.users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=255, required=False)
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "department",
            "year",
            "student_id",
            "photo",
            "phone",
            "is_active",
            "password",
            "is_accept_kvkk",
            "is_accept_user_agreement",
        ]


class RegisterSerializer(DefaultRegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    student_id = serializers.CharField()
    is_accept_kvkk = serializers.BooleanField()
    is_accept_user_agreement = serializers.BooleanField()

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
        }

    def save(self, request):
        user = super(RegisterSerializer, self).save(request)
        data = {
            "student_id": self.validated_data.get("student_id", ""),
            "is_accept_kvkk": self.validated_data.get("is_accept_kvkk", False),
            "is_accept_user_agreement": self.validated_data.get(
                "is_accept_user_agreement", False
            ),
        }

        for key, value in data.items():
            setattr(user, key, value)
        user.save(update_fields=data.keys())
        return user
