from django.db.transaction import atomic

from app.events.models import Event
from app.tickets import exceptions
from app.tickets.models import Ticket
from app.users.models import User


class TicketService(object):
    @staticmethod
    def create_ticket(event: Event, user: User) -> Ticket:
        try:
            Ticket.objects.get(event=event, user=user)
            raise exceptions.TicketAlreadyExist(params={"event_title": event.title})
        except Ticket.DoesNotExist:
            pass
        ticket = Ticket(event=event, user=user)

        with atomic():
            ticket.save()

        return ticket

    @staticmethod
    def delete_ticket(ticket: Ticket) -> None:
        ticket.delete()
