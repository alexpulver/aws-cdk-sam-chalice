import os

from chalicelib import users


def init_users_repository() -> users.UsersRepository:
    dynamodb_database = users.DynamoDBDatabase(os.environ["TABLE_NAME"])
    users_repository = users.UsersRepository(database=dynamodb_database)
    return users_repository
