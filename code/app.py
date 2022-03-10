from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler import AppSyncResolver
from aws_lambda_powertools.utilities.data_classes.appsync import scalar_types_utils
from resolvers.create_user_account import create_user_account as createUserAccount
from resolvers.update_user_account import update_user_account as updateUserAccount
from resolvers.delete_user_account import delete_user_account as deleteUserAccount
from resolvers.get_user import get_user as getUser

tracer = Tracer(service="app_resolver")
logger = Logger(service="app_resolver")
app = AppSyncResolver()


@app.resolver(type_name="Mutation", field_name="createUser")
def create_user(user: dict):
    user: dict = {"id": scalar_types_utils.make_id(), "age": 30, "country": "Cameroon", "favouriteMeal": "Achu",
                  "firstName": "Rosius", "lastName": "Ndimofor Ateh", "village": "Akum"}
    logger.debug(f' user data :{user}')
    return user


# return createUserAccount(user)


@app.resolver(type_name="Mutation", field_name="updateUser")
def update_user(input: {}):
    if input is None:
        input = {}
    return updateUserAccount()


@app.resolver(type_name="Mutation", field_name="deleteUser")
def delete_user(id: str = ""):
    return deleteUserAccount()


@app.resolver(type_name="Query", field_name="getUser")
def get_user(id: str = ""):
    return getUser()


@logger.inject_lambda_context(correlation_id_path=correlation_paths.APPSYNC_RESOLVER)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    return app.resolve(event, context)
