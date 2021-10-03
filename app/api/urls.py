from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from app.events.resources.views import EventViewSet
from app.news.resources.views import NewsViewSet
from app.tickets.resources.views import TicketViewSet
from app.users.resources.views import UserViewSet

router_v1 = routers.SimpleRouter()
router_v1.register(r"users", UserViewSet)
router_v1.register(r"tickets", TicketViewSet)
router_v1.register(r"events", EventViewSet)
router_v1.register(r"news", NewsViewSet)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/", include("dj_rest_auth.urls")),
    path("v1/auth/registration/", include("dj_rest_auth.registration.urls")),

    path("password-reset/confirm/<uidb64>/<token>/",
         TemplateView.as_view(template_name="password_reset_confirm.html"),
         name='password_reset_confirm'),
]
