from typing import Dict

from aws_lambda_powertools import Logger, Tracer
import boto3
import os

from decimal import *
from aws_lambda_powertools.utilities.data_classes.appsync import scalar_types_utils
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")

logger = Logger(service="create_user_account")
tracer = Tracer(service="create_user_account")

table = dynamodb.Table(os.environ["TABLE_NAME"])


@tracer.capture_method
def create_user_account(input: Dict = None):
    if input is None:
        input = {}
    user = {
        "id": scalar_types_utils.make_id(),
        "firstName": input['firstName'],
        "lastName": input['lastName'],
        "favouriteMeal": input['favouriteMeal'],
        "country": input['country'],
        "village": input['village'],
        "age": input['age'],

    }
    logger.debug(f'user input :{user}')
    try:

        response = table.put_item(
            Item={
                **user
            }
        )

        logger.info(" create user account response {}".format(response))
        return user

    except ClientError as err:
        logger.debug(f"Error occurred during user account creation {err.response['Error']}")
        raise err
