from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from app.events.models import Event
from app.events.resources.serializers import EventSerializer
from app.events.service import EventService


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    service = EventService()

    def perform_create(self, serializer):
        data = serializer.validated_data
        self.service.create_event(**data)

    def perform_update(self, serializer):
        data = serializer.validated_data
        event = self.get_object()
        self.service.update_event(event, **data)

    def perform_destroy(self, instance):
        raise MethodNotAllowed(method="DELETE")
