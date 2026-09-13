from src.database.connection import get_db

STATUS_VALIDOS = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]


def create(usuario_id, itens):
    """Cria um pedido de forma transacional, validando estoque e preços."""
    db = get_db()
    cursor = db.cursor()

    total = 0
    linhas = []
    for item in itens:
        cursor.execute(
            "SELECT id, nome, preco, estoque FROM produtos WHERE id = ?",
            (item["produto_id"],),
        )
        produto = cursor.fetchone()
        if produto is None:
            return {"erro": f"Produto {item['produto_id']} não encontrado"}
        if produto["estoque"] < item["quantidade"]:
            return {"erro": f"Estoque insuficiente para {produto['nome']}"}
        total += produto["preco"] * item["quantidade"]
        linhas.append((produto["id"], produto["preco"], item["quantidade"]))

    try:
        cursor.execute(
            "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
            (usuario_id, total),
        )
        pedido_id = cursor.lastrowid
        for produto_id, preco, quantidade in linhas:
            cursor.execute(
                "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, "
                "preco_unitario) VALUES (?, ?, ?, ?)",
                (pedido_id, produto_id, quantidade, preco),
            )
            cursor.execute(
                "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                (quantidade, produto_id),
            )
        db.commit()
    except Exception:
        db.rollback()
        raise

    return {"pedido_id": pedido_id, "total": total}


def _montar_pedidos(rows_pedidos, cursor):
    """Monta pedidos com seus itens usando uma única query de itens (evita N+1)."""
    pedidos = {}
    ordem = []
    for row in rows_pedidos:
        pedidos[row["id"]] = {
            "id": row["id"],
            "usuario_id": row["usuario_id"],
            "status": row["status"],
            "total": row["total"],
            "criado_em": row["criado_em"],
            "itens": [],
        }
        ordem.append(row["id"])

    if not ordem:
        return []

    placeholders = ",".join("?" for _ in ordem)
    cursor.execute(
        f"""
        SELECT ip.pedido_id, ip.produto_id, ip.quantidade, ip.preco_unitario,
               p.nome AS produto_nome
        FROM itens_pedido ip
        LEFT JOIN produtos p ON p.id = ip.produto_id
        WHERE ip.pedido_id IN ({placeholders})
        """,
        ordem,
    )
    for item in cursor.fetchall():
        pedidos[item["pedido_id"]]["itens"].append(
            {
                "produto_id": item["produto_id"],
                "produto_nome": item["produto_nome"] or "Desconhecido",
                "quantidade": item["quantidade"],
                "preco_unitario": item["preco_unitario"],
            }
        )

    return [pedidos[pid] for pid in ordem]


def get_by_user(usuario_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM pedidos WHERE usuario_id = ?", (usuario_id,))
    return _montar_pedidos(cursor.fetchall(), cursor)


def get_all():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM pedidos")
    return _montar_pedidos(cursor.fetchall(), cursor)


def update_status(pedido_id, novo_status):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id)
    )
    db.commit()
    return True


def sales_report():
    cursor = get_db().cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_pedidos,
            COALESCE(SUM(total), 0) AS faturamento,
            SUM(CASE WHEN status = 'pendente' THEN 1 ELSE 0 END) AS pendentes,
            SUM(CASE WHEN status = 'aprovado' THEN 1 ELSE 0 END) AS aprovados,
            SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END) AS cancelados
        FROM pedidos
        """
    )
    row = cursor.fetchone()
    total_pedidos = row["total_pedidos"]
    faturamento = row["faturamento"] or 0

    if faturamento > 10000:
        desconto = faturamento * 0.1
    elif faturamento > 5000:
        desconto = faturamento * 0.05
    elif faturamento > 1000:
        desconto = faturamento * 0.02
    else:
        desconto = 0

    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": round(faturamento, 2),
        "desconto_aplicavel": round(desconto, 2),
        "faturamento_liquido": round(faturamento - desconto, 2),
        "pedidos_pendentes": row["pendentes"] or 0,
        "pedidos_aprovados": row["aprovados"] or 0,
        "pedidos_cancelados": row["cancelados"] or 0,
        "ticket_medio": round(faturamento / total_pedidos, 2) if total_pedidos > 0 else 0,
    }
