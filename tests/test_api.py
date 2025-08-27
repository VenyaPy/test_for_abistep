import os
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))
from fastapi_server.app.main import app  # noqa: E402
from fastapi_server.app.storage import storage  # noqa: E402


@pytest.fixture(autouse=True)
def setup_api_key():
    os.environ["API_KEY"] = "test-key"
    # reset storage
    storage._users.clear()
    storage._email_index.clear()
    storage._next_id = 1
    yield

@pytest.fixture
def client():
    return TestClient(app)


def auth_headers():
    return {"x-api-key": os.environ["API_KEY"]}


def test_create_and_list_users(client):
    resp = client.post("/users", json={"name": "Alice", "email": "alice@example.com", "balance": 100}, headers=auth_headers())
    assert resp.status_code == 201
    resp = client.get("/users", headers=auth_headers())
    data = resp.json()
    assert len(data) == 1
    assert data[0]["email"] == "alice@example.com"


def test_unique_email(client):
    client.post("/users", json={"name": "Alice", "email": "alice@example.com", "balance": 100}, headers=auth_headers())
    resp = client.post("/users", json={"name": "Bob", "email": "alice@example.com", "balance": 50}, headers=auth_headers())
    assert resp.status_code == 400


def test_transfer(client):
    client.post("/users", json={"name": "Alice", "email": "alice@example.com", "balance": 100}, headers=auth_headers())
    client.post("/users", json={"name": "Bob", "email": "bob@example.com", "balance": 50}, headers=auth_headers())
    resp = client.post("/transfer", json={"from_user_id": 1, "to_user_id": 2, "amount": 30}, headers=auth_headers())
    assert resp.status_code == 200
    resp = client.get("/users", headers=auth_headers())
    balances = [u["balance"] for u in resp.json()]
    assert balances == [70.0, 80.0]


def test_transfer_self_forbidden(client):
    client.post("/users", json={"name": "Alice", "email": "alice@example.com", "balance": 100}, headers=auth_headers())
    resp = client.post("/transfer", json={"from_user_id": 1, "to_user_id": 1, "amount": 10}, headers=auth_headers())
    assert resp.status_code == 400


def test_transfer_insufficient_funds(client):
    client.post("/users", json={"name": "Alice", "email": "alice@example.com", "balance": 10}, headers=auth_headers())
    client.post("/users", json={"name": "Bob", "email": "bob@example.com", "balance": 50}, headers=auth_headers())
    resp = client.post("/transfer", json={"from_user_id": 1, "to_user_id": 2, "amount": 30}, headers=auth_headers())
    assert resp.status_code == 400


def test_ping_and_auth(client):
    resp = client.get("/ping", headers=auth_headers())
    assert resp.status_code == 200
    resp = client.get("/ping")
    assert resp.status_code == 401
