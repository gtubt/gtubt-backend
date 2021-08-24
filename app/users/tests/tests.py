import io
import os

from django.test import TestCase
from model_bakery import baker

from app.users.exceptions import UserDuplicatedFieldException
from app.users.resources.serializers import UserSerializer
from app.users.service import UserService


class UserServiceTestCase(TestCase):
    service = UserService()
    serializer = UserSerializer

    def setUp(self):
        self.data = {
            "name": "first_name",
            "last_name": "last_name",
            "department": "cse",
            "year": 1,
            "email": "test@gtubt.com",
            "student_id": "12104400",
            "is_active": True,
            "phone": "5555555555",
            "password": "passwordTest",
        }
        self.image_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "tests/data/300x300.png",
        )

    def test_create_user(self):
        serializer = self.serializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        user = self.service.create_user(**serializer.validated_data)
        self.assertEqual(user.email, self.data["email"])

    def test_create_user_with_existing_user(self):
        serializer = self.serializer(data=self.data)
        self.assertTrue(serializer.is_valid())

        self.service.create_user(**serializer.validated_data)

        with self.assertRaises(UserDuplicatedFieldException):
            self.service.create_user(**serializer.validated_data)

    def test_update_user(self):
        serializer = self.serializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        user = self.service.create_user(**serializer.validated_data)
        self.assertEqual(user.email, self.data["email"])

        data = self.serializer(user).data
        update_data = {"year": 2, "department": "eee"}

        serializer = self.serializer(instance=user, data=data)
        self.assertTrue(serializer.is_valid())
        update_user = self.service.update_user(user, **update_data)
        self.assertEqual(update_data["department"], update_user.department)

    def test_update_user_with_avatar(self):
        with io.open(self.image_path, "rb") as f:
            serializer = self.serializer(data=self.data)
            self.assertTrue(serializer.is_valid())
            user = self.service.create_user(**serializer.validated_data)
            updated_data = dict(photo=f.read())
            user = self.service.update_user(user=user, **updated_data)
            self.assertIsNotNone(user.photo)

    def test_delete_user(self):
        user = baker.make("users.User", email="test@gtubt.com", is_active=True)
        self.service.delete_user(user)
        user.refresh_from_db()
        self.assertFalse(user.is_active)
