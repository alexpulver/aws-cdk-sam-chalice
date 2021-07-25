from chalice import Chalice
from chalice import Response
from chalicelib.wrappers import UsersDatabaseDynamoDBEngine

app = Chalice(app_name="API")


@app.route("/users", methods=["POST"])
def create_user() -> Response:
    user_attributes = app.current_request.json_body
    username = user_attributes["username"]
    del user_attributes["username"]

    users_database = UsersDatabaseDynamoDBEngine()
    user = users_database.get_user(username)
    if user:
        return Response(f"User {username} already exists", status_code=400)
    else:
        created_user = users_database.create_user(username, user_attributes)
        return Response(created_user)


@app.route("/users/{username}", methods=["PUT"])
def update_user(username: str) -> Response:
    user_attributes = app.current_request.json_body
    users_database = UsersDatabaseDynamoDBEngine()
    updated_user = users_database.update_user(username, user_attributes)
    return Response(updated_user)


@app.route("/users/{username}", methods=["GET"])
def get_user(username: str) -> Response:
    users_database = UsersDatabaseDynamoDBEngine()
    user = users_database.get_user(username)
    if not user:
        return Response(f"User {username} does not exist", status_code=404)
    else:
        return Response(user)


@app.route("/users/{username}", methods=["DELETE"])
def delete_user(username: str) -> Response:
    users_database = UsersDatabaseDynamoDBEngine()
    if not users_database.get_user(username):
        return Response(f"User {username} does not exist", status_code=404)
    else:
        users_database.delete_user(username)
        return Response(f"User {username} was deleted", status_code=200)
