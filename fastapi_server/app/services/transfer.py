from ..storage import storage


def transfer(from_user_id: int, to_user_id: int, amount: float) -> None:
    storage.transfer(from_user_id, to_user_id, amount)
