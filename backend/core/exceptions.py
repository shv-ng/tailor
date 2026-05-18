import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response:
        return response

    logger.error(exc)

    return Response(
        {
            "detail": str(exc),
            "type": exc.__class__.__name__,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
