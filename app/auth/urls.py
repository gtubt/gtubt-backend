from dj_rest_auth.views import LoginView, UserDetailsView, PasswordResetView, \
    PasswordResetConfirmView, PasswordChangeView
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from rest_auth.views import LogoutView

from app.auth.views import EmailVerificationSentView

urlpatterns = [
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(),
         name='rest_password_reset_confirm'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('registration/', include("dj_rest_auth.registration.urls")),

    path("confirm-email", EmailVerificationSentView,
         name="account_email_verification_sent"),

    # to send verification email etc.
    # path("", include("allauth.urls")),

    # this url is used to generate email content
    re_path(r"^password-reset/confirm/(?P<uidb64>[0-9]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,48})/$",        # NoQA
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),
]
