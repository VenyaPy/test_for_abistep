from ..models import User, UserCreate
from ..storage import storage


def create_user(user: UserCreate) -> User:
    return storage.create_user(user)


def list_users() -> list[User]:
    return storage.list_users()
