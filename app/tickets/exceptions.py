from app.exceptions import codes
from app.exceptions.exceptions import PBaseException


class TicketAlreadyExist(PBaseException):
    code = codes.ticket_100_1
