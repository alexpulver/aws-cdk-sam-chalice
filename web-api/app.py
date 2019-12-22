import os

from chalice import Chalice, Response

from chalicelib.dynamodb_users_database import DynamoDbUsersDatabase
from chalicelib.users import Users


app = Chalice(app_name='aws-cdk-sam-chalice-web-api')
dynamodb_users_database = DynamoDbUsersDatabase(os.environ['DYNAMODB_TABLE_NAME'])
users = Users(dynamodb_users_database)


@app.route('/users', methods=['POST'])
def create_user() -> Response:
    user_attributes = app.current_request.json_body
    username = user_attributes['username']
    del user_attributes['username']

    user = users.get_user(username)
    if user:
        return Response(f'User {username} already exists', status_code=400)
    else:
        created_user = users.create_user(username, user_attributes)
        return Response(created_user)


@app.route('/users/{username}', methods=['PUT'])
def update_user(username: str) -> Response:
    user_attributes = app.current_request.json_body

    updated_user = users.update_user(username, user_attributes)

    return Response(updated_user)


@app.route('/users/{username}', methods=['GET'])
def get_user(username: str) -> Response:
    user = users.get_user(username)
    if not user:
        return Response(f'User {username} does not exist', status_code=404)
    else:
        return Response(user)


@app.route('/users/{username}', methods=['DELETE'])
def delete_user(username: str) -> Response:
    if not users.get_user(username):
        return Response(f'User {username} does not exist', status_code=404)
    else:
        users.delete_user(username)
        return Response(f'User {username} was deleted', status_code=200)
