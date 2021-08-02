from django.db.transaction import atomic

from app.users import exceptions
from app.users.enums import Department
from app.users.models import User


class UserService(object):
    @staticmethod
    def create_user(
        name: str,
        last_name: str,
        department: Department.choices,
        email: str,
        student_id: str,
        photo_url: str,
        phone: str,
        **kwargs: dict,
    ) -> User:
        try:
            User.objects.get(email=email)
            raise exceptions.UserDuplicatedFieldException()
        except User.DoesNotExist:
            pass

        user = User(
            name=name,
            last_name=last_name,
            department=department,
            email=email,
            student_id=student_id,
            photo_url=photo_url,
            phone=phone,
            **kwargs,
        )
        with atomic():
            user.save()
        return user

    @staticmethod
    def update_user(user: User, **kwargs: dict) -> User:
        kwargs.pop("id", None)
        new_email = kwargs.pop("email", None)
        try:
            User.objects.exclude(email=user.email).get(email=new_email)
            raise exceptions.UserDuplicatedFieldException()
        except User.DoesNotExist:
            pass

        for key, value in kwargs.items():
            setattr(user, key, value)

        with atomic():
            user.save(update_fields=kwargs.keys())
        return user

    @staticmethod
    def delete_user(user: User):
        user.is_active = False
        user.save(update_fields=["is_active"])
