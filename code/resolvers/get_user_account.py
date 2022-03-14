from aws_lambda_powertools import Logger, Tracer
import boto3
import os

from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
tracer = Tracer(service="get_user")
logger = Logger(service="get_user")

table = dynamodb.Table(os.environ["TABLE_NAME"])


@tracer.capture_method
def get_user_account(id: str = ""):
    logger.debug(f'user id is:{id}')
    try:
        response = table.get_item(
            Key={
                'id': id,

            }
        )
        logger.debug("user dict {}".format(response))
        if response['Item'] is None:
            logger.debug("response is null")
            return {}
        else:
            logger.debug("response is not null")

            return response['Item']
    except ClientError as err:
        logger.debug(f"Error occurred during get users item {err.response['Error']}")
        raise err
