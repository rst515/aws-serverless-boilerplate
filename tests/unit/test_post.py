import unittest
from http import HTTPStatus
from unittest.mock import Mock

from aws_lambda_powertools.utilities.typing import LambdaContext
from moto import mock_aws

from src.services.api.post import handler


@mock_aws
class TestPostHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.context = Mock(spec=LambdaContext)

    def test_post_handler(self):
        result = handler({"body": '{"id": "123", "name": "test"}'}, self.context)
        self.assertEqual(HTTPStatus.OK, result["statusCode"])
