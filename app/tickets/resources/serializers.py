from rest_framework import serializers

from app.events.models import Event
from app.tickets.models import Ticket
from app.users.models import User


class SubEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("title", "date")


class SubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "last_name")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("event", "user")


class TicketDetailedSerializer(TicketSerializer):
    event = SubEventSerializer
    user = SubUserSerializer
