import inspect
import json
from http import HTTPStatus
from typing import Any, Union, Dict, List

from src.logger import get_logger, SERVICE_ERROR

LOGGER = get_logger(__name__)

STATUS_CODE = "statusCode"
MESSAGE = "message"


class Messages:  # pylint:disable=too-few-public-methods
    NOT_FOUND = "Not found"


class Errors:  # pylint:disable=too-few-public-methods
    INTERNAL_SERVER_ERROR = "Internal Server Error"


def response(status_code: int, body: Union[Dict, List] = None) -> dict:
    resp: Dict[str, Any] = {
        STATUS_CODE: status_code
    }

    if body is not None:
        resp["body"] = json.dumps(body)

    return resp


def internal_server_error(status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR, body: object = None) -> dict:
    LOGGER.error(SERVICE_ERROR, inspect.stack()[1].function, status_code, body)
    return response(HTTPStatus.INTERNAL_SERVER_ERROR, {MESSAGE: Errors.INTERNAL_SERVER_ERROR})


def success(body: Union[Dict, List] = None) -> dict:
    return response(HTTPStatus.OK, body)


def created(body: dict) -> dict:
    return response(HTTPStatus.CREATED, body)


def not_found(message: str = Messages.NOT_FOUND) -> dict:
    return response(HTTPStatus.NOT_FOUND, {MESSAGE: message})


def no_content() -> dict:
    return response(HTTPStatus.NO_CONTENT)


def bad_request(status_code: HTTPStatus, message: str) -> dict:
    LOGGER.error(SERVICE_ERROR, inspect.stack()[1].function, status_code, message)
    return response(HTTPStatus.BAD_REQUEST, {MESSAGE: message})
