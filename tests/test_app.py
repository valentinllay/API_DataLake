import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_hello(client):
    rv = client.get("/")
    assert rv.data == b"Hello World"
    assert rv.status_code == 200
