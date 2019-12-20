from abc import ABC, abstractmethod
from typing import Dict


class UsersDatabase(ABC):
    @abstractmethod
    def create_user(self, username: str, user_attributes: Dict[str, str]) -> Dict[str, str]:
        pass

    @abstractmethod
    def update_user(self, username: str, user_attributes: Dict[str, str]) -> Dict[str, str]:
        pass

    @abstractmethod
    def get_user(self, username: str) -> Dict[str, str]:
        pass

    @abstractmethod
    def delete_user(self, username: str) -> None:
        pass
