from typing import Dict, List

from .models import User, UserCreate


class UserStorage:
    """In-memory storage for users."""

    def __init__(self) -> None:
        self._users: Dict[int, User] = {}
        self._email_index: Dict[str, int] = {}
        self._next_id = 1

    def list_users(self) -> List[User]:
        return list(self._users.values())

    def create_user(self, data: UserCreate) -> User:
        if data.email in self._email_index:
            raise ValueError("Email already exists")
        user = User(id=self._next_id, **data.model_dump())
        self._users[self._next_id] = user
        self._email_index[data.email] = self._next_id
        self._next_id += 1
        return user

    def get_user(self, user_id: int) -> User:
        return self._users.get(user_id)

    def transfer(self, from_id: int, to_id: int, amount: float) -> None:
        from_user = self._users.get(from_id)
        to_user = self._users.get(to_id)
        if from_user is None or to_user is None:
            raise ValueError("User not found")
        if from_id == to_id:
            raise ValueError("Cannot transfer to self")
        if from_user.balance < amount:
            raise ValueError("Insufficient funds")
        from_user.balance -= amount
        to_user.balance += amount


storage = UserStorage()
