import os
from typing import Any, Dict, Type

from chalicelib.database_engine import DynamoDBEngine
from chalicelib.users_database import UsersDatabase


class UsersDatabaseSingletonMeta(type):
    _instances: Dict[Type[Any], object] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> object:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class UsersDatabaseDynamoDBEngine(UsersDatabase, metaclass=UsersDatabaseSingletonMeta):
    """Implement as singleton to initialize the SDK client only once."""

    def __init__(self) -> None:
        super().__init__(database_engine=DynamoDBEngine(os.environ["TABLE_NAME"]))
