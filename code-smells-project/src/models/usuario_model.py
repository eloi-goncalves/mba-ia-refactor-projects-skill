from werkzeug.security import check_password_hash, generate_password_hash

from src.database.connection import get_db

# Campos públicos — a senha (hash) nunca é exposta.
_COLUNAS_PUBLICAS = ["id", "nome", "email", "tipo", "criado_em"]


def _to_public_dict(row):
    return {coluna: row[coluna] for coluna in _COLUNAS_PUBLICAS}


def get_all():
    cursor = get_db().cursor()
    cursor.execute("SELECT id, nome, email, tipo, criado_em FROM usuarios")
    return [_to_public_dict(row) for row in cursor.fetchall()]


def get_by_id(usuario_id):
    cursor = get_db().cursor()
    cursor.execute(
        "SELECT id, nome, email, tipo, criado_em FROM usuarios WHERE id = ?",
        (usuario_id,),
    )
    row = cursor.fetchone()
    return _to_public_dict(row) if row else None


def create(nome, email, senha, tipo="cliente"):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome, email, generate_password_hash(senha), tipo),
    )
    db.commit()
    return cursor.lastrowid


def authenticate(email, senha):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    row = cursor.fetchone()
    if row and check_password_hash(row["senha"], senha):
        return {
            "id": row["id"],
            "nome": row["nome"],
            "email": row["email"],
            "tipo": row["tipo"],
        }
    return None
