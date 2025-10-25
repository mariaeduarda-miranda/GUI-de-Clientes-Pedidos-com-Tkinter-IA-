import sqlite3
from sqlite3 import Error

DB_NAME = "clientes_pedidos.db"

def get_connection():
    """Retorna conexão com o banco SQLite."""
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

def init_db():
    """Inicializa o banco com as tabelas necessárias."""
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT,
                    telefone TEXT
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER,
                    data TEXT,
                    total REAL,
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS itens_pedido (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pedido_id INTEGER,
                    produto TEXT,
                    quantidade INTEGER,
                    preco_unit REAL,
                    FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
                );
            """)
            conn.commit()
        except Error as e:
            print(f"Erro ao criar tabelas: {e}")
        finally:
            conn.close()

def execute_query(query, params=(), fetch=False):
    """Executa comandos SQL com tratamento de erros."""
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        if fetch:
            data = cur.fetchall()
            conn.close()
            return data
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print(f"Erro SQL: {e}")
        return None
