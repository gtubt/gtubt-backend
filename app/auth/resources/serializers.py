from dj_rest_auth.serializers import \
    PasswordResetSerializer as DefaultPasswordResetSerializer
from django.contrib.auth.forms import PasswordResetForm
from django.db.models import Q

from app.auth.exceptions import AuthUserInactiveException
from app.users.models import User


class PasswordResetSerializer(DefaultPasswordResetSerializer):

    def get_email_options(self):
        return {
            'html_email_template_name': 'registration/password_reset_email.html',
            'subject_template_name': 'registration/password_reset_subject.txt',
        }

    @property
    def password_reset_form_class(self):
        return PasswordResetForm

    def validate_email(self, value):
        user = User.objects.filter(
            Q(username=value) | Q(email=value)).distinct().first()
        if user:
            if not user.is_active:
                raise AuthUserInactiveException()
        else:
            raise AuthUserInactiveException()
        return super(PasswordResetSerializer, self).validate_email(value)
