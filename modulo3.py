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

def validar_cpf(cpf):
    cpf_limpo = cpf.replace(".", "").replace("-", "")
    if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
        return False
    return True


def cadastrar_cliente(nome, cpf, email="", tipo_desconto_id=None):
    if not validar_cpf(cpf):
        print("CPF inválido. Digite 11 números.")
        return

    conn = get_conexao()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO clientes (nome, cpf, email, tipo_desconto_id) VALUES (?, ?, ?, ?)",
            (nome, cpf, email, tipo_desconto_id)
        )
        conn.commit()
        print(f"Cliente '{nome}' cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print(f"Erro: O CPF {cpf} já está cadastrado no sistema.")
    except Exception as e:
        print(f"Erro ao cadastrar cliente: {e}")
    finally:
        conn.close()


def listar_cliente():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT clientes.*, tipos_desconto.nome AS desconto, tipos_desconto.percentual
        FROM clientes
        LEFT JOIN tipos_desconto ON clientes.tipo_desconto_id = tipos_desconto.id
        ORDER BY clientes.nome
    """)
    clientes = cursor.fetchall()
    conn.close()
    return clientes


def buscar_cliente_por_cpf(cpf):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT clientes.*, tipos_desconto.nome AS desconto, tipos_desconto.percentual
        FROM clientes
        LEFT JOIN tipos_desconto ON clientes.tipo_desconto_id = tipos_desconto.id 
        WHERE clientes.cpf = ?
    """, (cpf,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente


def atualizar_pontos(cliente_id, pontos_a_adicionar):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE clientes SET pontos_fidelidade = pontos_fidelidade + ? WHERE id = ?",
        (pontos_a_adicionar, cliente_id)
    )
    conn.commit()
    conn.close()


def remover_cliente(cpf):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM clientes WHERE cpf = ?", (cpf,))
    cliente = cursor.fetchone()
    if not cliente:
        print("Cliente não encontrado!")
        conn.close()
        return
    cursor.execute("DELETE FROM clientes WHERE cpf = ?", (cpf,))
    conn.commit()
    conn.close()
    print(f"Cliente '{cliente['nome']}' removido!")


# ==========================================
# GERENCIAMENTO DE DESCONTOS
# ==========================================

def cadastrar_tipo_desconto(nome, percentual):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tipos_desconto (nome, percentual) VALUES (?, ?)",
        (nome, percentual)
    )
    conn.commit()
    conn.close()
    print(f"Desconto '{nome}' ({percentual}%) cadastrado!")


def listar_tipos_desconto():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tipos_desconto")
    descontos = cursor.fetchall()
    conn.close()
    return descontos


def atualizar_tipo_desconto(desconto_id, novo_nome=None, novo_percentual=None):
    conn = get_conexao()
    cursor = conn.cursor()
    if novo_percentual is not None:
        cursor.execute("UPDATE tipos_desconto SET percentual = ? WHERE id = ?", (novo_percentual, desconto_id))
    if novo_nome is not None:
        cursor.execute("UPDATE tipos_desconto SET nome = ? WHERE id = ?", (novo_nome, desconto_id))
    conn.commit()
    conn.close()
    print(f"Desconto ID {desconto_id} atualizado")


def remover_tipo_desconto(desconto_id):
    conn = get_conexao()
    cursor = conn.cursor()

    # Verifica se algum cliente está usando este desconto antes de excluir
    cursor.execute("SELECT COUNT(*) as total FROM clientes WHERE tipo_desconto_id = ?", (desconto_id,))
    resultado = cursor.fetchone()

    if resultado['total'] > 0:
        print("Não é possível remover este desconto pois há clientes cadastrados com ele.")
    else:
        cursor.execute("DELETE FROM tipos_desconto WHERE id = ?", (desconto_id,))
        conn.commit()
        print("Desconto removido com sucesso!")
    conn.close()


def calcular_preco_final(preco_base, cliente_cpf=None):
    if not cliente_cpf:
        return preco_base

    cliente = buscar_cliente_por_cpf(cliente_cpf)
    if cliente and cliente["percentual"]:
        desconto = cliente["percentual"] / 100
        preco_final = preco_base * (1 - desconto)
        print(f"Desconto de {cliente['percentual']}% aplicado: R$ {preco_final:.2f}")
        return preco_final
    return preco_base


# ==========================================
# REGRAS DO PROGRAMA DE FIDELIDADE
# ==========================================

PONTOS_POR_REAL = 1
VALOR_POR_PONTO = 0.10


def adicionar_pontos(cliente_id, valor_compra, descricao="Compra de ingresso"):
    pontos_ganhos = int(valor_compra * PONTOS_POR_REAL)
    if pontos_ganhos <= 0:
        return

    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE clientes SET pontos_fidelidade = pontos_fidelidade + ? WHERE id = ?",
        (pontos_ganhos, cliente_id)
    )

    cursor.execute(
        "INSERT INTO fidelidade_transacoes (cliente_id, pontos, tipo, descricao, data) VALUES (?, ?, ?, ?, ?)",
        (cliente_id, pontos_ganhos, "ganho", descricao, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )

    conn.commit()
    conn.close()
    print(f"+{pontos_ganhos} pontos adicionados!")


def calcular_desconto_por_pontos(pontos):
    return pontos * VALOR_POR_PONTO


def resgatar_pontos(cliente_cpf, pontos_a_resgatar):
    cliente = buscar_cliente_por_cpf(cliente_cpf)

    if not cliente:
        print("Cliente não encontrado!")
        return 0.0

    if cliente["pontos_fidelidade"] < pontos_a_resgatar:
        print(f"Pontos insuficientes! Saldo atual: {cliente['pontos_fidelidade']} pontos.")
        return 0.0

    desconto = calcular_desconto_por_pontos(pontos_a_resgatar)

    conn = get_conexao()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE clientes SET pontos_fidelidade = pontos_fidelidade - ? WHERE id = ?",
        (pontos_a_resgatar, cliente["id"])
    )

    cursor.execute(
        "INSERT INTO fidelidade_transacoes (cliente_id, pontos, tipo, descricao, data) VALUES (?, ?, ?, ?, ?)",
        (cliente["id"], -pontos_a_resgatar, "resgate",
         f"Resgate de {pontos_a_resgatar} pontos = R$ {desconto:.2f} de desconto",
         datetime.now().strftime("%Y-%m-%d %H:%M"))
    )

    conn.commit()
    conn.close()
    print(f"{pontos_a_resgatar} pontos resgatados! Desconto de R$ {desconto:.2f} aplicado.")
    return desconto


def ver_saldo(cliente_cpf):
    cliente = buscar_cliente_por_cpf(cliente_cpf)

    if not cliente:
        print("Cliente não encontrado!")
        return

    pontos = cliente["pontos_fidelidade"]
    valor = calcular_desconto_por_pontos(pontos)
    print(f"\nPONTOS DE FIDELIDADE — {cliente['nome']}")
    print(f"   Saldo:      {pontos} pontos")
    print(f"   Equivale a: R$ {valor:.2f} em desconto\n")


def ver_historico(cliente_cpf):
    cliente = buscar_cliente_por_cpf(cliente_cpf)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pontos, tipo, descricao, data
        FROM fidelidade_transacoes
        WHERE cliente_id = ?
        ORDER BY data DESC
    """, (cliente["id"],))
    transacoes = cursor.fetchall()
    conn.close()

    print(f"\nHISTÓRICO DE PONTOS — {cliente['nome']}")
    print(f"   Saldo atual: {cliente['pontos_fidelidade']} pontos\n")

    if not transacoes:
        print("   Nenhuma transação ainda.")
        return

    for t in transacoes:
        sinal = "+" if t["tipo"] == "ganho" else "-"
        emoji = "⭐" if t["tipo"] == "ganho" else "🎟️"
        print(f"   {emoji} {sinal}{abs(t['pontos'])} pontos | {t['descricao']} | {t['data']}")
    print()


# ==========================================
# INICIALIZAÇÃO OBRIGATÓRIA
# ==========================================
# Executa a criação das tabelas toda vez que o arquivo rodar
setup_clientes_db()

# Espaço livre para fazer testes de terminal aqui embaixo: