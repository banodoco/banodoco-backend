import json
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse


def success(payload, message, status_bool):
    response = {
        'payload': payload,
        'message': message,
        'status': status_bool
    }

    return Response(response, status=status.HTTP_200_OK)


def bad_request(payload):
    response = {
        'payload': payload,
        'message': 'invalid request',
        'status': False
    }

    return Response(response, status=status.HTTP_400_BAD_REQUEST)


# Using http reponse because of SentryMiddleware
def error(payload):
    response = {
        'payload': payload,
        'message': 'could not process the request. please try again',
        'status': False
    }

    return HttpResponse(
        json.dumps(response),
        content_type="application/json",
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def unauthorized(payload):
    response = {
        'payload': payload,
        'message': 'not authorized',
        'status': False
    }

    return Response(response, status=status.HTTP_401_UNAUTHORIZED)


def forbidden(payload):
    response = {
        'payload': payload,
        'message': 'not have enough have permission',
        'status': False
    }

    return Response(response, status=status.HTTP_403_FORBIDDEN)
