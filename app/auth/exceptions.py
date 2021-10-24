from app.exceptions import codes
from app.exceptions.exceptions import PBaseException


class AuthUserInactiveException(PBaseException):
    code = codes.auth_100_1
