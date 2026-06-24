import sqlite3


def setup_db_modulo3():
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()

    # Tabela de Clientes (Programa de Fidelidade)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL
        )
    """)

    # Tabela de Tickets (Ingressos vendidos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            seat_code TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions (id_session)
        )
    """)

    conexao.commit()
    conexao.close()


def cadastrar_cliente(nome, cpf):
    """Cadastra um novo cliente no programa de fidelidade."""
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()
    try:
        cursor.execute("INSERT INTO clientes (nome, cpf) VALUES (?, ?)", (nome, cpf))
        conexao.commit()
        return True, "Cliente cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        # Se tentar cadastrar um CPF que já existe, o banco avisa!
        return False, "Erro: CPF já cadastrado no sistema."
    finally:
        conexao.close()


def verificar_fidelidade(cpf):
    """Verifica se o CPF existe no banco para aplicar o desconto de R$ 5,00."""
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clientes WHERE cpf = ?", (cpf,))
    cliente = cursor.fetchone()
    conexao.close()

    if cliente:
        return True  # O cliente existe, tem direito ao desconto!
    return False  # Não existe, paga o valor normal.


def registrar_venda_no_banco(id_sessao, lista_assentos):
    """Módulo 3: Responsável estritamente por processar e salvar as vendas de ingressos"""
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    for assento in lista_assentos:
        cursor.execute("INSERT INTO tickets (session_id, seat_code) VALUES (?, ?)", (id_sessao, assento))

    conexao.commit()
    conexao.close()


# Executa a criação das tabelas toda vez que o módulo for importado
setup_db_modulo3()

