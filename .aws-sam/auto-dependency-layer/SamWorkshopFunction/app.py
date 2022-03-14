from typing import Dict

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler import AppSyncResolver
from resolvers.create_user_account import create_user_account as createUserAccount
from resolvers.get_user_account import get_user_account as getUserAccount

tracer = Tracer(service="sample_resolver")
logger = Logger(service="sample_resolver")

from aws_lambda_powertools.utilities.data_classes.appsync import scalar_types_utils

app = AppSyncResolver()


# Note that `creation_time` isn't available in the schema

@app.resolver(type_name="Mutation", field_name="createUser")
def create_user(user: Dict):
    return createUserAccount(user)


@app.resolver(type_name="Mutation", field_name="updateUser")
def update_user(user_input: Dict):
    return updateUserAccount(user_input)


@app.resolver(type_name="Query", field_name="getUser")
def get_user(id: str = ""):
    return getUserAccount(id)


@logger.inject_lambda_context(correlation_id_path=correlation_paths.APPSYNC_RESOLVER)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    return app.resolve(event, context)
