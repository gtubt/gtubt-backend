from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated

from app.tickets.models import Ticket
from app.tickets.resources.serializers import TicketDetailedSerializer, TicketSerializer
from app.tickets.service import TicketService
from core.utils.viewsets import MultiSerializerViewSetMixin


class TicketViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    service = TicketService()
    queryset = Ticket.objects.select_related("user", "event").all()
    serializer_action_classes = {
        "detailed": TicketDetailedSerializer,
        "detailed-list": TicketDetailedSerializer,
    }
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.is_valid()
        self.service.create_ticket(**serializer.validated_data)

    def perform_update(self, serializer):
        raise MethodNotAllowed(method="PATCH")

    def perform_destroy(self, instance):
        self.service.delete_ticket(instance)
