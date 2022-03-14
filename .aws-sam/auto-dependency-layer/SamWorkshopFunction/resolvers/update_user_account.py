from typing import Dict

from aws_lambda_powertools import Logger, Tracer
import boto3
import os

from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
tracer = Tracer(service="get_user")
logger = Logger(service="get_user")

table = dynamodb.Table(os.environ["TABLE_NAME"])


def update_user_account(user_input: Dict):
    if user_input is None:
        userInput = {}
    logger.info(f"user data is {user_input}")

    user: Dict = {
        "firstName": user_input['firstName'],
        "lastName": user_input['lastName'],
        "favouriteMeal": user_input['favouriteMeal'],
        "country": user_input['country'],
        "village": user_input['village'],
        "age": user_input['age'],
    }

    try:
        response = table.update_item(
            Key={
                'id': user_input["id"]
            },
            ConditionExpression="attribute_exists(id)",
            UpdateExpression="set firstName= :firstName,lastName= :lastName, "
                             "favouriteMeal= :favouriteMeal, country= :country, village= :village,"
                             "age= :age",
            ExpressionAttributeValues={
                ":firstName": user['firstName'],
                ":lastName": user['lastName'],
                ":favouriteMeal": user['favouriteMeal'],
                ":country": user["country"],
                ":village": user['village'],
                ":age": user["age"]
            },
            ReturnValues="ALL_NEW"
        )
        logger.debug({' update response': response['Attributes']})
        return response['Attributes']

    except ClientError as err:
        logger.debug(f"Error occurred during user update{err.response['Error']}")
        raise
