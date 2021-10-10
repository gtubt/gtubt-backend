from django.urls import path, include
from rest_framework import routers

from app.user_account.resources.views import AccountViewSet

router = routers.SimpleRouter()
router.register(r"", AccountViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include("allauth.urls"))
]
