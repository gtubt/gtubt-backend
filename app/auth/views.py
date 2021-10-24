from allauth.account.views import (
    EmailVerificationSentView as BaseEmailVerificationSentView,
)


class EmailVerificationSentView(BaseEmailVerificationSentView):
    template_name = "account/verification_sent.html"
