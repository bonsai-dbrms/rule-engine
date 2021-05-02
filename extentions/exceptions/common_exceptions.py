from rest_framework import status
from rest_framework.exceptions import APIException, NotFound, ParseError, ValidationError


class ResourceConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Record already exists."

    def __init__(self, fields=None):
        if fields is not None:
            self.detail += " Duplicate Value for: %s" % (str(fields))


class NetworkException(APIException):
    pass


class ResourceNotFoundException(NotFound):
    pass


class ParseException(ParseError):
    pass


class BadRequestException(ValidationError):
    pass
