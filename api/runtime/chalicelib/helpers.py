import os

from chalicelib.users import DynamoDBDatabase
from chalicelib.users import Users


def init_users_repository() -> Users:
    dynamodb_database = DynamoDBDatabase(os.environ["TABLE_NAME"])
    users = Users(database=dynamodb_database)
    return users
