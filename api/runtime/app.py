import chalice
from chalicelib import helpers

app = chalice.Chalice(app_name="API")


@app.route("/users", methods=["POST"])
def create_user() -> chalice.Response:
    user_attributes = app.current_request.json_body
    username = user_attributes["username"]
    del user_attributes["username"]

    users_repository = helpers.init_users_repository()
    user = users_repository.get_user(username)
    if user:
        return chalice.Response(f"User {username} already exists", status_code=400)
    else:
        created_user = users_repository.create_user(username, user_attributes)
        return chalice.Response(created_user)


@app.route("/users/{username}", methods=["PUT"])
def update_user(username: str) -> chalice.Response:
    user_attributes = app.current_request.json_body
    users_repository = helpers.init_users_repository()
    updated_user = users_repository.update_user(username, user_attributes)
    return chalice.Response(updated_user)


@app.route("/users/{username}", methods=["GET"])
def get_user(username: str) -> chalice.Response:
    users_repository = helpers.init_users_repository()
    user = users_repository.get_user(username)
    if not user:
        return chalice.Response(f"User {username} does not exist", status_code=404)
    else:
        return chalice.Response(user)


@app.route("/users/{username}", methods=["DELETE"])
def delete_user(username: str) -> chalice.Response:
    users_repository = helpers.init_users_repository()
    if not users_repository.get_user(username):
        return chalice.Response(f"User {username} does not exist", status_code=404)
    else:
        users_repository.delete_user(username)
        return chalice.Response(f"User {username} was deleted", status_code=200)
