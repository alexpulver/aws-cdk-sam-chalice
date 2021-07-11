from typing import Any, Dict, Optional

from chalicelib.database_engine import DatabaseEngineInterface


class UsersDatabase:
    def __init__(self, *, database_engine: DatabaseEngineInterface) -> None:
        self._database_engine = database_engine

    def create_user(
        self, username: str, user_attributes: Dict[str, str]
    ) -> Dict[str, str]:
        return self._database_engine.create_user(username, user_attributes)

    def update_user(self, username: str, user_attributes: Dict[str, str]) -> Any:
        return self._database_engine.update_user(username, user_attributes)

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        return self._database_engine.get_user(username)

    def delete_user(self, username: str) -> None:
        self._database_engine.delete_user(username)
