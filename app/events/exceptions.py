from app.exceptions import codes
from app.exceptions.exceptions import PBaseException


class EventDuplicatedFieldException(PBaseException):
    code = codes.event_100_1
