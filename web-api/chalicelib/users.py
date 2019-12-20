from typing import Dict

from chalicelib.users_database import UsersDatabase


class Users:
    def __init__(self, database: UsersDatabase) -> None:
        self._database = database

    def create_user(self, username: str, user_attributes: Dict[str, str]) -> Dict[str, str]:
        return self._database.create_user(username, user_attributes)

    def update_user(self, username: str, user_attributes: Dict[str, str]) -> Dict[str, str]:
        return self._database.update_user(username, user_attributes)

    def get_user(self, username: str) -> Dict[str, str]:
        return self._database.get_user(username)

    def delete_user(self, username: str) -> None:
        self._database.delete_user(username)
