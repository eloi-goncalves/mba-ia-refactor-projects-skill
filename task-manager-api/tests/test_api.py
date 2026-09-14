import os
import tempfile

os.environ["DATABASE_URI"] = "sqlite:///" + tempfile.mktemp(suffix=".db")
os.environ["SECRET_KEY"] = "test-secret"

import pytest  # noqa: E402

from app import app as flask_app  # noqa: E402


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_criar_usuario_nao_expoe_password(client):
    resp = client.post(
        "/users", json={"name": "Ana", "email": "ana@x.com", "password": "1234"}
    )
    assert resp.status_code == 201
    assert "password" not in resp.get_json()
    lista = client.get("/users")
    for usuario in lista.get_json():
        assert "password" not in usuario


def test_login_com_hash(client):
    client.post("/users", json={"name": "Bia", "email": "bia@x.com", "password": "abcd"})
    ok = client.post("/login", json={"email": "bia@x.com", "password": "abcd"})
    assert ok.status_code == 200
    bad = client.post("/login", json={"email": "bia@x.com", "password": "errada"})
    assert bad.status_code == 401


def test_task_overdue_calculado(client):
    client.post("/categories", json={"name": "Backend", "color": "#3498db"})
    client.post("/users", json={"name": "U", "email": "u@e.com", "password": "1234"})
    resp = client.post(
        "/tasks",
        json={"title": "Task antiga", "user_id": 1, "category_id": 1,
              "due_date": "2020-01-01", "priority": 1},
    )
    assert resp.status_code == 201
    assert resp.get_json()["overdue"] is True


def test_reports_summary(client):
    resp = client.get("/reports/summary")
    assert resp.status_code == 200
    assert "user_productivity" in resp.get_json()
