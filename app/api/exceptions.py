from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as rest_exception_handler
from rest_framework.views import set_rollback

from app.exceptions.exceptions import PBaseException


def custom_exception_handler(exc, context):
    if isinstance(exc, PBaseException):
        # TODO: translate msg
        data = {"error_code": exc.code["code"], "error_msg": exc.message}
        set_rollback()
        return Response(data=data, status=status.HTTP_406_NOT_ACCEPTABLE)


def exception_handler(exc, context):
    response = rest_exception_handler(exc, context)
    if response is None:
        response = custom_exception_handler(exc, context)

    return response
