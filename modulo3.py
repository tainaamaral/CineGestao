import sqlite3
from datetime import datetime


# ==========================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ==========================================

# Conecta no mesmo arquivo criado no Módulo 1
def get_conexao():
    conn = sqlite3.connect('banco.db')
    # Permite acessar colunas pelo nome (ex: cliente['nome']) em vez de índices
    conn.row_factory = sqlite3.Row
    return conn

def setup_clientes_db():
    conn = get_conexao()
    cursor = conn.cursor()

    # Cria a tabela de Tipos de Desconto
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tipos_desconto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            percentual REAL NOT NULL
        )
    """)

    # Cria a tabela de Clientes (com Chave Estrangeira ligando aos descontos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            email TEXT,
            tipo_desconto_id INTEGER,
            pontos_fidelidade INTEGER DEFAULT 0,
            FOREIGN KEY(tipo_desconto_id) REFERENCES tipos_desconto(id)
        )
    """)

    # Cria a tabela de Histórico de Fidelidade
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fidelidade_transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            pontos INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            descricao TEXT,
            data TEXT,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id)
        )
    """)

    conn.commit()
    conn.close()


# ==========================================
# GERENCIAMENTO DE CLIENTES
# ==========================================
