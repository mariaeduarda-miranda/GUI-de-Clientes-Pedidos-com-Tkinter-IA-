from db import execute_query
from db import execute_query

# ---------- CLIENTES ----------
def inserir_cliente(nome, email, telefone):
    return execute_query(
        "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
        (nome, email, telefone)
    )

def atualizar_cliente(cliente_id, nome, email, telefone):
    return execute_query(
        "UPDATE clientes SET nome=?, email=?, telefone=? WHERE id=?",
        (nome, email, telefone, cliente_id)
    )

def excluir_cliente(cliente_id):
    return execute_query("DELETE FROM clientes WHERE id=?", (cliente_id,))

def listar_clientes(filtro=""):
    if filtro:
        like = f"%{filtro}%"
        return execute_query(
            "SELECT * FROM clientes WHERE nome LIKE ? OR email LIKE ? ORDER BY nome",
            (like, like),
            fetch=True
        )
    return execute_query("SELECT * FROM clientes ORDER BY nome", fetch=True)

def obter_cliente(cliente_id):
    data = execute_query("SELECT * FROM clientes WHERE id=?", (cliente_id,), fetch=True)
    return data[0] if data else None


# ---------- PEDIDOS ----------
def inserir_pedido(cliente_id, data, total, itens):
    """Insere pedido e seus itens de forma transacional."""
    from db import get_connection
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO pedidos (cliente_id, data, total) VALUES (?, ?, ?)",
            (cliente_id, data, total)
        )
        pedido_id = cur.lastrowid
        for item in itens:
            cur.execute(
                "INSERT INTO itens_pedido (pedido_id, produto, quantidade, preco_unit) VALUES (?, ?, ?, ?)",
                (pedido_id, item['produto'], item['quantidade'], item['preco_unit'])
            )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Erro ao salvar pedido: {e}")
        return False
    finally:
        conn.close()

def listar_pedidos(data_inicio=None, data_fim=None):
    query = "SELECT p.id, c.nome, p.data, p.total FROM pedidos p JOIN clientes c ON c.id = p.cliente_id"
    params = []
    if data_inicio and data_fim:
        query += " WHERE date(p.data) BETWEEN date(?) AND date(?)"
        params = [data_inicio, data_fim]
    query += " ORDER BY p.data DESC"
    return execute_query(query, params, fetch=True)