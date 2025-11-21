import sqlite3

DB_NAME = "loja.db"


def get_connection():
    """Retorna uma conexão com o banco de dados."""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Inicializa o banco de dados criando as tabelas necessárias."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela Clientes (id, nome, email, telefone)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT
        )
    ''')

    # Tabela Pedidos (id, cliente_id, data, total)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id)
        )
    ''')

    # Tabela Itens do Pedido
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unit REAL NOT NULL,
            FOREIGN KEY(pedido_id) REFERENCES pedidos(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso.")


if __name__ == "__main__":
    init_db()