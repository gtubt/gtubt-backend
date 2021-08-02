from django.test import TestCase
from model_bakery import baker

from app.events.models import Event
from app.tickets.exceptions import TicketAlreadyExist
from app.tickets.models import Ticket
from app.tickets.resources.serializers import TicketSerializer
from app.tickets.service import TicketService
from app.users.models import User


class TicketTestCase(TestCase):
    service = TicketService()
    serializer = TicketSerializer

    def setUp(self) -> None:
        self.user = baker.make("users.User", name="Özlem", last_name="Türeci")
        self.event = baker.make("events.Event", title="Event Title")

    def test_create_ticket(self):
        data = {
            "user": self.user.id,
            "event": self.event.id,
        }

        serializer = self.serializer(data=data)
        self.assertTrue(serializer.is_valid())
        ticket = self.service.create_ticket(**serializer.validated_data)
        self.assertEqual(ticket.user.name, self.user.name)
        self.assertEqual(ticket.event.title, self.event.title)

    def test_delete_ticket(self):
        ticket = baker.make("tickets.Ticket", user=self.user, event=self.event)
        ticket_id = ticket.id
        self.service.delete_ticket(ticket)
        with self.assertRaises(Ticket.DoesNotExist):
            Ticket.objects.get(id=ticket_id)

        user = User.objects.filter(email=self.user.email)
        self.assertTrue(user.exists())

        event = Event.objects.filter(id=self.event.id)
        self.assertTrue(event.exists())

    def test_create_test_with_already_exist(self):
        data = {
            "user": self.user.id,
            "event": self.event.id,
        }

        serializer = self.serializer(data=data)
        self.assertTrue(serializer.is_valid())
        ticket = self.service.create_ticket(**serializer.validated_data)
        self.assertEqual(ticket.user.name, self.user.name)
        self.assertEqual(ticket.event.title, self.event.title)

        with self.assertRaises(TicketAlreadyExist):
            self.service.create_ticket(**serializer.validated_data)
