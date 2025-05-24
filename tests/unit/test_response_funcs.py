import json
import unittest
from http import HTTPStatus

from src.response_funcs import (
    Errors,
    MESSAGE,
    Messages,
    bad_request,
    created,
    internal_server_error,
    no_content,
    not_found,
    response as response_func,
    success,
)


class TestResponseFuncs(unittest.TestCase):

    def test_response_func__with_body(self):
        response = response_func(
            status_code=HTTPStatus.OK,
            body={"message": "Hello World!"}
        )
        self.assertEqual(response["statusCode"], HTTPStatus.OK)
        self.assertEqual(response["body"], '{"message": "Hello World!"}')
        self.assertTrue(json.loads(response.get("body")))

    def test_response_func__without_body(self):
        response = response_func(
            status_code=HTTPStatus.OK,
            body=None
        )
        self.assertEqual(response["statusCode"], HTTPStatus.OK)
        self.assertIsNone(response.get("body"))

    def test_internal_server_error_default(self):
        result = internal_server_error()
        self.assertEqual(result["statusCode"], HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual({MESSAGE: Errors.INTERNAL_SERVER_ERROR}, json.loads(result["body"]))

    def test_success_with_body(self):
        body = {"key": "value"}
        result = success(body)
        self.assertEqual(result["statusCode"], HTTPStatus.OK)
        self.assertEqual(body, json.loads(result["body"]))

    def test_success_without_body(self):
        result = success()
        self.assertEqual(result["statusCode"], HTTPStatus.OK)
        self.assertIsNone(result.get("body"))

    def test_created(self):
        body = {"id": 1}
        result = created(body)
        self.assertEqual(result["statusCode"], HTTPStatus.CREATED)
        self.assertEqual(body, json.loads(result["body"]))

    def test_not_found_default(self):
        result = not_found()
        self.assertEqual(result["statusCode"], HTTPStatus.NOT_FOUND)
        self.assertEqual({MESSAGE: Messages.NOT_FOUND}, json.loads(result["body"]))

    def test_not_found_custom_message(self):
        msg = "Custom not found"
        result = not_found(msg)
        self.assertEqual(result["statusCode"], HTTPStatus.NOT_FOUND)
        self.assertEqual({MESSAGE: msg}, json.loads(result["body"]))

    def test_no_content(self):
        result = no_content()
        self.assertEqual(result["statusCode"], HTTPStatus.NO_CONTENT)
        self.assertIsNone(result.get("body"))

    def test_bad_request(self):
        msg = "Invalid input"
        result = bad_request(HTTPStatus.BAD_REQUEST, msg)
        self.assertEqual(result["statusCode"], HTTPStatus.BAD_REQUEST)
        self.assertEqual({MESSAGE: msg}, json.loads(result["body"]))
