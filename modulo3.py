import sqlite3


def setup_db_modulo3():
    """Cria as tabelas do Módulo 3 caso elas não existam."""
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






# Conecta no mesmo arquivo criado no Módulo 1
# def get_conexao():
#     conn = sqlite3.connect('banco.db')
#     # Permite acessar colunas pelo nome (ex: cliente['nome']) em vez de índices
#     conn.row_factory = sqlite3.Row
#     return conn
#
# def setup_clientes_db():
#     conn = get_conexao()
#     cursor = conn.cursor()
#
#     # 1. Cria a tabela de descontos
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS tipos_desconto (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             nome TEXT NOT NULL,
#             percentual REAL NOT NULL
#         )
#     """)
#
#     # 2. Popula os descontos padrão automaticamente se a tabela estiver vazia
#     cursor.execute("SELECT COUNT(*) FROM tipos_desconto")
#     if cursor.fetchone()[0] == 0:
#         cursor.execute("INSERT INTO tipos_desconto (id, nome, percentual) VALUES (1, 'Nenhum', 0)")
#         cursor.execute("INSERT INTO tipos_desconto (id, nome, percentual) VALUES (2, 'Estudante (50%)', 50)")
#         cursor.execute("INSERT INTO tipos_desconto (id, nome, percentual) VALUES (3, 'Idoso (50%)', 50)")
#         cursor.execute("INSERT INTO tipos_desconto (id, nome, percentual) VALUES (4, 'Fidelidade (20%)', 20)")
#
#     # 3. Cria a tabela de clientes
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS clientes (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             nome TEXT NOT NULL,
#             cpf TEXT UNIQUE NOT NULL,
#             email TEXT,
#             tipo_desconto_id INTEGER,
#             pontos_fidelidade INTEGER DEFAULT 0,
#             FOREIGN KEY(tipo_desconto_id) REFERENCES tipos_desconto(id)
#         )
#     """)
#
#     conn.commit()
#     conn.close()
#
# # GERENCIAMENTO DE CLIENTES
# def validar_cpf(cpf):
#     cpf_limpo = cpf.replace(".", "").replace("-", "")
#     if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
#         return False
#     return True
#
#
# def cadastrar_cliente(nome, cpf, email="", tipo_desconto_id=None):
#     if not validar_cpf(cpf):
#         print("CPF inválido. Digite 11 números.")
#         return
#
#     conn = get_conexao()
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO clientes (nome, cpf, email, tipo_desconto_id) VALUES (?, ?, ?, ?)",
#             (nome, cpf, email, tipo_desconto_id)
#         )
#         conn.commit()
#         print(f"Cliente '{nome}' cadastrado com sucesso!")
#     except sqlite3.IntegrityError:
#         print(f"Erro: O CPF {cpf} já está cadastrado no sistema.")
#     except Exception as e:
#         print(f"Erro ao cadastrar cliente: {e}")
#     finally:
#         conn.close()
#
#
# def listar_cliente():
#     conn = get_conexao()
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT clientes.*, tipos_desconto.nome AS desconto, tipos_desconto.percentual
#         FROM clientes
#         LEFT JOIN tipos_desconto ON clientes.tipo_desconto_id = tipos_desconto.id
#         ORDER BY clientes.nome
#     """)
#     clientes = cursor.fetchall()
#     conn.close()
#     return clientes
#
#
# def buscar_cliente_por_cpf(cpf):
#     conn = get_conexao()
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT clientes.*, tipos_desconto.nome AS desconto, tipos_desconto.percentual
#         FROM clientes
#         LEFT JOIN tipos_desconto ON clientes.tipo_desconto_id = tipos_desconto.id
#         WHERE clientes.cpf = ?
#     """, (cpf,))
#     cliente = cursor.fetchone()
#     conn.close()
#     return cliente
#
#
# def atualizar_pontos(cliente_id, pontos_a_adicionar):
#     conn = get_conexao()
#     cursor = conn.cursor()
#     cursor.execute(
#         "UPDATE clientes SET pontos_fidelidade = pontos_fidelidade + ? WHERE id = ?",
#         (pontos_a_adicionar, cliente_id)
#     )
#     conn.commit()
#     conn.close()
#
#
# def remover_cliente(cpf):
#     conn = get_conexao()
#     cursor = conn.cursor()
#     cursor.execute("SELECT nome FROM clientes WHERE cpf = ?", (cpf,))
#     cliente = cursor.fetchone()
#     if not cliente:
#         print("Cliente não encontrado!")
#         conn.close()
#         return
#     cursor.execute("DELETE FROM clientes WHERE cpf = ?", (cpf,))
#     conn.commit()
#     conn.close()
#     print(f"Cliente '{cliente['nome']}' removido!")
#
#
# # GERENCIAMENTO DE DESCONTOS
# def cadastrar_tipo_desconto(nome, percentual):
#     conn = get_conexao()
#     cursor = conn.cursor()
#     cursor.execute(
#         "INSERT INTO tipos_desconto (nome, percentual) VALUES (?, ?)",
#         (nome, percentual)
#     )
#     conn.commit()
#     conn.close()
#     print(f"Desconto '{nome}' ({percentual}%) cadastrado!")
#
#
# def listar_tipos_desconto():
#     conn = get_conexao()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM tipos_desconto")
#     descontos = cursor.fetchall()
#     conn.close()
#     return descontos
#
#
# def atualizar_tipo_desconto(desconto_id, novo_nome=None, novo_percentual=None):
#     conn = get_conexao()
#     cursor = conn.cursor()
#     if novo_percentual is not None:
#         cursor.execute("UPDATE tipos_desconto SET percentual = ? WHERE id = ?", (novo_percentual, desconto_id))
#     if novo_nome is not None:
#         cursor.execute("UPDATE tipos_desconto SET nome = ? WHERE id = ?", (novo_nome, desconto_id))
#     conn.commit()
#     conn.close()
#     print(f"Desconto ID {desconto_id} atualizado")
#
#
# def remover_tipo_desconto(desconto_id):
#     conn = get_conexao()
#     cursor = conn.cursor()
#
#     # Verifica se algum cliente está usando este desconto antes de excluir
#     cursor.execute("SELECT COUNT(*) as total FROM clientes WHERE tipo_desconto_id = ?", (desconto_id,))
#     resultado = cursor.fetchone()
#
#     if resultado['total'] > 0:
#         print("Não é possível remover este desconto pois há clientes cadastrados com ele.")
#     else:
#         cursor.execute("DELETE FROM tipos_desconto WHERE id = ?", (desconto_id,))
#         conn.commit()
#         print("Desconto removido com sucesso!")
#     conn.close()
#
#
# def calcular_preco_final(preco_base, cliente_cpf=None):
#     if not cliente_cpf:
#         return preco_base
#
#     cliente = buscar_cliente_por_cpf(cliente_cpf)
#     if cliente and cliente["percentual"]:
#         desconto = cliente["percentual"] / 100
#         preco_final = preco_base * (1 - desconto)
#         print(f"Desconto de {cliente['percentual']}% aplicado: R$ {preco_final:.2f}")
#         return preco_final
#     return preco_base
#
#
# # REGRAS DO PROGRAMA DE FIDELIDADE
# PONTOS_POR_REAL = 1
# VALOR_POR_PONTO = 0.10
#
#
# def adicionar_pontos(cliente_id, valor_compra, descricao="Compra de ingresso"):
#     pontos_ganhos = int(valor_compra * PONTOS_POR_REAL)
#     if pontos_ganhos <= 0:
#         return
#
#     conn = get_conexao()
#     cursor = conn.cursor()
#
#     cursor.execute(
#         "UPDATE clientes SET pontos_fidelidade = pontos_fidelidade + ? WHERE id = ?",
#         (pontos_ganhos, cliente_id)
#     )
#
#     cursor.execute(
#         "INSERT INTO fidelidade_transacoes (cliente_id, pontos, tipo, descricao, data) VALUES (?, ?, ?, ?, ?)",
#         (cliente_id, pontos_ganhos, "ganho", descricao, datetime.now().strftime("%Y-%m-%d %H:%M"))
#     )
#
#     conn.commit()
#     conn.close()
#     print(f"+{pontos_ganhos} pontos adicionados!")
#
#
# def calcular_desconto_por_pontos(pontos):
#     return pontos * VALOR_POR_PONTO
#
#
# def resgatar_pontos(cliente_cpf, pontos_a_resgatar):
#     cliente = buscar_cliente_por_cpf(cliente_cpf)
#
#     if not cliente:
#         print("Cliente não encontrado!")
#         return 0.0
#
#     if cliente["pontos_fidelidade"] < pontos_a_resgatar:
#         print(f"Pontos insuficientes! Saldo atual: {cliente['pontos_fidelidade']} pontos.")
#         return 0.0
#
#     desconto = calcular_desconto_por_pontos(pontos_a_resgatar)
#
#     conn = get_conexao()
#     cursor = conn.cursor()
#
#     cursor.execute(
#         "UPDATE clientes SET pontos_fidelidade = pontos_fidelidade - ? WHERE id = ?",
#         (pontos_a_resgatar, cliente["id"])
#     )
#
#     cursor.execute(
#         "INSERT INTO fidelidade_transacoes (cliente_id, pontos, tipo, descricao, data) VALUES (?, ?, ?, ?, ?)",
#         (cliente["id"], -pontos_a_resgatar, "resgate",
#          f"Resgate de {pontos_a_resgatar} pontos = R$ {desconto:.2f} de desconto",
#          datetime.now().strftime("%Y-%m-%d %H:%M"))
#     )
#
#     conn.commit()
#     conn.close()
#     print(f"{pontos_a_resgatar} pontos resgatados! Desconto de R$ {desconto:.2f} aplicado.")
#     return desconto
#
#
# def ver_saldo(cliente_cpf):
#     cliente = buscar_cliente_por_cpf(cliente_cpf)
#
#     if not cliente:
#         print("Cliente não encontrado!")
#         return
#
#     pontos = cliente["pontos_fidelidade"]
#     valor = calcular_desconto_por_pontos(pontos)
#     print(f"\nPONTOS DE FIDELIDADE — {cliente['nome']}")
#     print(f"   Saldo:      {pontos} pontos")
#     print(f"   Equivale a: R$ {valor:.2f} em desconto\n")
#
#
# def ver_historico(cliente_cpf):
#     cliente = buscar_cliente_por_cpf(cliente_cpf)
#
#     if not cliente:
#         print("Cliente não encontrado!")
#         return
#
#     conn = get_conexao()
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT pontos, tipo, descricao, data
#         FROM fidelidade_transacoes
#         WHERE cliente_id = ?
#         ORDER BY data DESC
#     """, (cliente["id"],))
#     transacoes = cursor.fetchall()
#     conn.close()
#
#     print(f"\nHISTÓRICO DE PONTOS — {cliente['nome']}")
#     print(f"   Saldo atual: {cliente['pontos_fidelidade']} pontos\n")
#
#     if not transacoes:
#         print("   Nenhuma transação ainda.")
#         return
#
#     for t in transacoes:
#         sinal = "+" if t["tipo"] == "ganho" else "-"
#         emoji = "⭐" if t["tipo"] == "ganho" else "🎟️"
#         print(f"   {emoji} {sinal}{abs(t['pontos'])} pontos | {t['descricao']} | {t['data']}")
#     print()
#
# # INICIALIZAÇÃO OBRIGATÓRIA
# setup_clientes_db()
