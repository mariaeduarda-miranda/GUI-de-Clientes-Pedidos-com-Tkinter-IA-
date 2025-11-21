import sqlite3
from db import get_connection
from datetime import datetime
import utils
# ... (Mantenha as funções CRUD de clientes/pedidos da Fase 1 aqui: criar_cliente, etc) ...

# --- Dashboard & Relatórios (Novas Funções) ---


DB_NAME = 'loja.db'


def get_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    return sqlite3.connect(DB_NAME)


# ... (outras funções CRUD, como inserir_cliente, atualizar_cliente, etc.)

# --- FUNÇÃO NECESSÁRIA PARA A BUSCA NA LISTAGEM ---
def get_todos_clientes(termo_busca=""):
    """
    Retorna todos os clientes, aplicando um filtro de busca no Nome ou Email.
    """
    conn = get_connection()
    cursor = conn.cursor()
    clientes = []

    try:
        if termo_busca:
            # Consulta com filtro (case-insensitive LIKE)
            termo = f'%{termo_busca}%'
            query = """
            SELECT id, nome, email, telefone 
            FROM clientes 
            WHERE nome LIKE ? OR email LIKE ?
            ORDER BY nome
            """
            cursor.execute(query, (termo, termo))
        else:
            # Consulta sem filtro
            query = "SELECT id, nome, email, telefone FROM clientes ORDER BY nome"
            cursor.execute(query)

        clientes = cursor.fetchall()

    except sqlite3.Error as e:
        utils.log_acao(f"Erro ao buscar todos os clientes: {e}")

    finally:
        conn.close()

    return clientes


# ... (restante do seu models.py)
def get_dashboard_stats():
    """
    Retorna estatísticas usando funções de agregação do SQLite (COUNT, AVG).
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Total de Clientes (Agregação: COUNT)
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cursor.fetchone()[0]

    # 2. Total de Pedidos no Mês
    # Obtém o ano e mês atual no formato 'YYYY-MM' para filtrar no SQLite
    mes_atual = datetime.now().strftime('%Y-%m')
    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE data LIKE ?", (f'{mes_atual}%',))
    total_pedidos_mes = cursor.fetchone()[0]

    # 3. Ticket Médio Geral (Agregação: AVG)
    # O SQL calcula a média automaticamente
    cursor.execute("SELECT AVG(total) FROM pedidos")
    resultado_ticket = cursor.fetchone()[0]

    # Se não houver pedidos, o AVG retorna None, então tratamos para 0.0
    ticket_medio = resultado_ticket if resultado_ticket else 0.0

    return total_clientes, total_pedidos_mes, ticket_medio

# --- Clientes ---
def criar_cliente(nome, email, telefone):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
                       (nome, email, telefone))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar cliente: {e}")
        raise
    finally:
        conn.close()


def listar_clientes(busca=""):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM clientes WHERE nome LIKE ? OR email LIKE ?"
    param = f"%{busca}%"
    cursor.execute(query, (param, param))
    dados = cursor.fetchall()
    conn.close()
    return dados


def excluir_cliente(cliente_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()


def atualizar_cliente(id, nome, email, telefone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE clientes SET nome=?, email=?, telefone=? WHERE id=?",
                   (nome, email, telefone, id))
    conn.commit()
    conn.close()


# --- Pedidos (Transacional) ---
def salvar_pedido_completo(cliente_id, data, total, itens):
    """Salva pedido e itens numa única transação."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Criar Pedido
        cursor.execute("INSERT INTO pedidos (cliente_id, data, total) VALUES (?, ?, ?)",
                       (cliente_id, data, total))
        pedido_id = cursor.lastrowid

        # 2. Criar Itens
        for item in itens:
            # item = (produto, quantidade, preco)
            cursor.execute("""
                INSERT INTO itens_pedido (pedido_id, produto, quantidade, preco_unit)
                VALUES (?, ?, ?, ?)
            """, (pedido_id, item[0], item[1], item[2]))

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def filtrar_pedidos(data_inicio, data_fim):
    """Filtra pedidos por intervalo de datas."""
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT p.id, c.nome, p.data, p.total 
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        WHERE p.data BETWEEN ? AND ?
    """
    cursor.execute(query, (data_inicio, data_fim))
    dados = cursor.fetchall()
    conn.close()
    return dados

def get_ultimos_pedidos(limite=5):
    """Pega os últimos X pedidos para a IA analisar."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, c.nome, p.total, p.data 
        FROM pedidos p 
        JOIN clientes c ON p.cliente_id = c.id
        ORDER BY p.id DESC LIMIT ?
    """, (limite,))
    dados = cursor.fetchall()
    conn.close()
    return dados

def get_dashboard_status():
    """Retorna estatísticas para o dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    # Total Clientes
    cursor.execute("SELECT COUNT(*) FROM clientes")

    # Total Pedidos
    cursor.execute("SELECT COUNT(*), SUM(total) FROM pedidos")
    qtd_pedidos, soma_vendas = cursor.fetchone()

    # Ticket Médio
    ticket_medio = (soma_vendas / qtd_pedidos) if qtd_pedidos else 0.0
    conn.close()
    return qtd_pedidos, ticket_medio


# --- Adicione isso ao final do models.py ---

def get_dados_para_analise_ia(limite=5):
    """
    Busca os últimos 5 pedidos E seus itens para enviar à IA.
    Retorna uma lista de strings formatadas.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Pega os IDs dos últimos 5 pedidos
    cursor.execute("SELECT id, data, total FROM pedidos ORDER BY id DESC LIMIT ?", (limite,))
    pedidos = cursor.fetchall()

    dados_formatados = []

    for ped in pedidos:
        ped_id, data, total = ped

        # Pega os itens desse pedido
        cursor.execute("SELECT produto, quantidade, preco_unit FROM itens_pedido WHERE pedido_id = ?", (ped_id,))
        itens = cursor.fetchall()

        itens_str = ", ".join([f"{i[1]}x {i[0]} (R${i[2]})" for i in itens])
        resumo = f"Pedido #{ped_id} ({data}): Total R${total:.2f} -> Itens: [{itens_str}]"
        dados_formatados.append(resumo)

    conn.close()
    return "\n".join(dados_formatados)