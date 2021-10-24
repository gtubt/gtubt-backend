from allauth.account.models import EmailAddress
from dj_rest_auth.views import LoginView as DefaultLoginView
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from app.users.models import User
from app.users.resources.serializers import UserSerializer
from app.users.service import UserService


class AccountViewSet(mixins.DestroyModelMixin, ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    service = UserService()

    def perform_destroy(self, instance):
        """
        :param instance: instance of User model
        """
        # TODO: to make anonymize??
        self.service.delete_user(instance)

    @action(detail=True, methods=["GET"], url_path="is-email-verified")
    def is_email_verified(self, request, *args, **kwargs):
        user = self.get_object()
        email_address = EmailAddress.objects.get(user.email)
        context = {"email_verified": email_address.verified}
        return Response(data=context)


class LoginView(DefaultLoginView):
    def process_login(self):
        if self.user.is_active:
            super(LoginView, self).process_login()
