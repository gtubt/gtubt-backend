from app.exceptions import codes
from app.exceptions.exceptions import PBaseException


class UserDuplicatedFieldException(PBaseException):
    code = codes.user_100_1
