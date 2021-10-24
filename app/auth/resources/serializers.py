from dj_rest_auth.serializers import \
    PasswordResetConfirmSerializer as DefaultPasswordResetConfirmSerializer
from dj_rest_auth.serializers import \
    PasswordResetSerializer as DefaultPasswordResetSerializer
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.db.models import Q
from django.utils.encoding import force_str
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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

    def save(self):
        from django.contrib.auth.tokens import default_token_generator

        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'token_generator': default_token_generator,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(DefaultPasswordResetConfirmSerializer):
    def validate(self, attrs):
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_decode as uid_decoder

        # Decode the uidb64 (allauth use base36) to uid to get User object

        try:
            uid = force_str(uid_decoder(attrs['uid']))
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs,
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs
