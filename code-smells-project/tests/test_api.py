import os
import tempfile

os.environ["DB_PATH"] = tempfile.mktemp(suffix=".db")
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


def test_listar_produtos(client):
    resp = client.get("/produtos")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["sucesso"] is True
    assert len(body["dados"]) >= 1


def test_login_com_hash_e_senha_errada(client):
    ok = client.post("/login", json={"email": "joao@email.com", "senha": "123456"})
    assert ok.status_code == 200
    bad = client.post("/login", json={"email": "joao@email.com", "senha": "errada"})
    assert bad.status_code == 401


def test_usuarios_nao_expoem_senha(client):
    resp = client.get("/usuarios")
    assert resp.status_code == 200
    for usuario in resp.get_json()["dados"]:
        assert "senha" not in usuario


def test_sql_injection_nao_vaza_dados(client):
    # Antes: concatenação permitiria injeção. Agora, parametrizado, retorna 404.
    resp = client.get("/produtos/0 OR 1=1")
    assert resp.status_code in (400, 404)


def test_criar_e_buscar_produto(client):
    criado = client.post(
        "/produtos",
        json={"nome": "Teclado Teste", "preco": 10.0, "estoque": 5, "categoria": "informatica"},
    )
    assert criado.status_code == 201
    novo_id = criado.get_json()["dados"]["id"]
    achado = client.get(f"/produtos/{novo_id}")
    assert achado.status_code == 200
