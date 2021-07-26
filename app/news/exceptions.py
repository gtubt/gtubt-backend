from app.exceptions import codes
from app.exceptions.exceptions import PBaseException


class NewsDuplicatedFieldException(PBaseException):
    code = codes.news_100_1
