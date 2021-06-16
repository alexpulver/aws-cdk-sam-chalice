from abc import ABC
from abc import abstractmethod
from typing import Any, Dict, Optional


class UsersDatabase(ABC):
    @abstractmethod
    def create_user(
        self, username: str, user_attributes: Dict[str, str]
    ) -> Dict[str, str]:
        pass

    @abstractmethod
    def update_user(self, username: str, user_attributes: Dict[str, str]) -> Any:
        pass

    @abstractmethod
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_user(self, username: str) -> None:
        pass
