from aws_lambda_powertools.utilities.typing import LambdaContext

from src.response_funcs import success
from src.services.common.powertools import logger, tracer, metrics
from src.logger import get_logger

LOGGER = get_logger(__name__)


@metrics.log_metrics
@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def handler(event: dict, context: LambdaContext) -> dict:  # pylint:disable=unused-argument
    LOGGER.info("Running post handler")
    return success(body={"message": "Success"})
