import uuid
from typing import Dict, List
from src.models.user import User

class UserRepository:
    """Manages storage for User objects in memory."""
    def __init__(self):
        self._users: Dict[uuid.UUID, User] = {}

    def add(self, user: User) -> None:
        """Adds a user to the repository."""
        if user.id in self._users:
            raise ValueError(f"User with ID {user.id} already exists.")
        self._users[user.id] = user

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Retrieves a user by their unique ID."""
        return self._users.get(user_id)

    def get_all(self) -> List[User]:
        """Returns a list of all users."""
        return list(self._users.values())
