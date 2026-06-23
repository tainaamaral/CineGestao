import customtkinter as ctk
import sqlite3

# Variáveis globais de controle da venda
id_sessao_atual = None
assentos_selecionados = []


def abrir_atendimento():
    ctk.set_appearance_mode("dark")

    app = ctk.CTk()
    app.geometry("1280x720")
    app.title("CineGestão - Frente de Caixa")
    app.configure(fg_color="#1A1A1A")

    # BASE DE DADOS: Garante de forma independente que a tabela de ingressos exista
    def garantir_tabela_ingressos():
        try:
            conexao = sqlite3.connect('banco.db')
            cursor = conexao.cursor()
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
        except Exception as e:
            print(f"Aviso na inicialização do banco: {e}")

    # TOPO DA TELA (Barra Superior com Botão Voltar integrado)
    top_frame = ctk.CTkFrame(app, height=60, fg_color="#000000", corner_radius=0)
    top_frame.pack(side="top", fill="x")

    def voltar_para_inicio():
        app.destroy()  # Fecha a tela de atendimento
        import main  # Recarrega o menu inicial do projeto
        main.iniciar_sistema()

    btn_voltar = ctk.CTkButton(top_frame, text="⬅ Voltar", width=90, height=35, fg_color="#242424",
                               hover_color="#333333", font=("Helvetica", 13, "bold"), command=voltar_para_inicio)
    btn_voltar.pack(side="left", padx=15, pady=12)

    titulo_topo = ctk.CTkLabel(top_frame, text="CINEGESTÃO - FRENTE DE CAIXA", font=("Helvetica", 20, "bold"),
                               text_color="#FFFFFF")
    titulo_topo.pack(pady=15, expand=True)

    # PAINEL ESQUERDO (Ações do Operador de Caixa)
    left_panel = ctk.CTkFrame(app, width=350, fg_color="#242424", corner_radius=0)
    left_panel.pack(side="left", fill="y")
    left_panel.pack_propagate(False)

    label_opcoes = ctk.CTkLabel(left_panel, text="Opções da Venda", font=("Helvetica", 24, "bold"),
                                text_color="#FFFFFF")
    label_opcoes.pack(pady=(30, 20))

    # BANCO DE DADOS: Carregar Filmes no Início
    def carregar_filmes_no_combo():
        try:
            conexao = sqlite3.connect('banco.db')
            cursor = conexao.cursor()
            cursor.execute("SELECT title FROM movies")
            filmes_do_banco = cursor.fetchall()
            conexao.close()

            lista_titulos = [filme[0] for filme in filmes_do_banco]
            if lista_titulos:
                combo_filme.configure(values=["Selecione o Filme"] + lista_titulos)
            else:
                combo_filme.configure(values=["Nenhum filme cadastrado"])
        except sqlite3.OperationalError:
            combo_filme.configure(values=["Banco de dados vazio"])

    # BANCO DE DADOS: Filtrar Sessões do Filme Escolhido
    def atualizar_combo_sessoes(escolha):
        filme_selecionado = combo_filme.get()
        if filme_selecionado in ["Selecione o Filme", "Nenhum filme cadastrado", "Banco de dados vazio"]:
            combo_sessao.configure(values=["Selecione a Sessão"])
            combo_sessao.set("Selecione a Sessão")
            alternar_sessao_e_construir_mapa()
            return

        try:
            conexao = sqlite3.connect('banco.db')
            cursor = conexao.cursor()
            query = """
                SELECT s.session_time, s.screen_number 
                FROM sessions s
                INNER JOIN movies m ON s.movie_id = m.id
                WHERE m.title = ?
            """
            cursor.execute(query, (filme_selecionado,))
            sessoes_encontradas = cursor.fetchall()
            conexao.close()

            lista_sessoes = [f"{s[0]} - Sala {s[1]}" for s in sessoes_encontradas]

            if lista_sessoes:
                combo_sessao.configure(values=lista_sessoes)
                combo_sessao.set(lista_sessoes[0])
                alternar_sessao_e_construir_mapa(lista_sessoes[0])
            else:
                combo_sessao.configure(values=["Sem sessões disponíveis"])
                combo_sessao.set("Sem sessões disponíveis")
                alternar_sessao_e_construir_mapa()
        except sqlite3.OperationalError:
            combo_sessao.configure(values=["Erro ao ler sessões"])
            alternar_sessao_e_construir_mapa()

    # BANCO DE DADOS: Gerar Mapa Reativo com Letras (A-J) e Números (1-80)
    def alternar_sessao_e_construir_mapa(escolha=None):
        global id_sessao_atual
        sessao_selecionada = combo_sessao.get()

        assentos_ocupados_no_banco = []
        id_sessao_atual = None

        if sessao_selecionada and sessao_selecionada not in ["Selecione a Sessão", "Sem sessões disponíveis",
                                                             "Erro ao ler sessões"]:
            try:
                partes = sessao_selecionada.split(" - Sala ")
                horario = partes[0]
                sala_num = int(partes[1])

                conexao = sqlite3.connect('banco.db')
                cursor = conexao.cursor()

                cursor.execute("""
                    SELECT id_session FROM sessions 
                    WHERE session_time = ? AND screen_number = ?
                """, (horario, sala_num))
                dados_sessao = cursor.fetchone()

                if dados_sessao:
                    id_sessao_atual = dados_sessao[0]
                    cursor.execute("SELECT seat_code FROM tickets WHERE session_id = ?", (id_sessao_atual,))
                    assentos_ocupados_no_banco = [row[0] for row in cursor.fetchall()]

                conexao.close()
            except Exception as e:
                print(f"Erro ao ler assentos ocupados: {e}")

        for widget in matriz_frame.winfo_children():
            widget.destroy()

        assentos_selecionados.clear()
        label_assento.configure(text="Assento Selecionado: --")

        letras_fileiras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        linhas = 10
        assentos_por_linha = 8

        for fileira in range(linhas):
            lbl_letra = ctk.CTkLabel(matriz_frame, text=letras_fileiras[fileira], font=("Helvetica", 16, "bold"),
                                     text_color="#A0A0A0", width=30)
            lbl_letra.grid(row=fileira, column=0, padx=(0, 15), pady=5)

            for assento in range(assentos_por_linha):
                num_poltrona = (fileira * assentos_por_linha) + assento + 1
                nome_assento = str(num_poltrona)

                if nome_assento in assentos_ocupados_no_banco:
                    cor_fundo = "#810000"
                    cor_hover = "#630000"
                    cor_texto = "#EEEBDD"
                else:
                    cor_fundo = "#EEEBDD"
                    cor_hover = "#CFCAC0"
                    cor_texto = "#1B1717"

                btn_poltrona = ctk.CTkButton(matriz_frame,
                                             text=nome_assento,
                                             width=42,
                                             height=42,
                                             corner_radius=8,
                                             fg_color=cor_fundo,
                                             hover_color=cor_hover,
                                             text_color=cor_texto,
                                             font=("Helvetica", 11, "bold"))

                btn_poltrona.configure(command=lambda f=fileira, a=assento, b=btn_poltrona: clicar_poltrona(f, a, b))
                btn_poltrona.grid(row=fileira, column=assento + 1, padx=5, pady=5)

        atualizar_resumo_venda()

    def atualizar_resumo_venda(escolha_do_combo=None):
        filme = combo_filme.get()
        sessao = combo_sessao.get()
        ingresso = combo_ingresso.get()

        if not assentos_selecionados or sessao in ["Selecione a Sessão",
                                                   "Sem sessões disponíveis"] or filme == "Selecione o Filme":
            label_total.configure(text="Total a Pagar: R$ 0,00", text_color="#FFFFFF")
            return

        try:
            partes = sessao.split(" - Sala ")
            horario = partes[0]
            sala = int(partes[1])

            conexao = sqlite3.connect('banco.db')
            cursor = conexao.cursor()
            cursor.execute("SELECT base_price FROM sessions WHERE session_time = ? AND screen_number = ?",
                           (horario, sala))
            resultado = cursor.fetchone()
            conexao.close()

            if resultado:
                preco_base = resultado[0]
                if "Meia-Entrada" in ingresso:
                    preco_base /= 2

                total = preco_base * len(assentos_selecionados)
                label_total.configure(text=f"Total a Pagar: R$ {total:.2f}", text_color="#FFFFFF")
        except Exception:
            label_total.configure(text="Total a Pagar: R$ 0,00", text_color="#FFFFFF")

    # SIMULAÇÃO DO CARTÃO IMPRESSO (Recebe os assentos fixos salvos)
    def abrir_modal_bilhete(assentos_emitidos):
        modal = ctk.CTkToplevel(app)
        modal.geometry("460x580")
        modal.title("Emissão de Bilhete")
        modal.configure(fg_color="#222222")
        modal.resizable(False, False)

        modal.lift()
        modal.attributes("-topmost", True)
        modal.focus_force()
        modal.grab_set()

        app.janela_modal_ativa = modal

        texto_filme = combo_filme.get()
        texto_sessao = combo_sessao.get()
        assentos_ordenados = sorted(assentos_emitidos, key=int)
        texto_assentos = ", ".join(assentos_ordenados)
        texto_total = label_total.cget("text").replace("Total a Pagar: ", "")

        cartao_ingresso = ctk.CTkFrame(modal, fg_color="#FFFDF0", corner_radius=12, border_width=2,
                                       border_color="#D5D1C3")
        cartao_ingresso.pack(pady=25, padx=25, fill="both", expand=True)

        ctk.CTkLabel(cartao_ingresso, text="⭐ CINEGESTÃO BILHETEIRA ⭐", font=("Courier New", 16, "bold"),
                     text_color="#1B1717").pack(pady=(20, 5))
        ctk.CTkLabel(cartao_ingresso, text="-----------------------------------", font=("Courier New", 12),
                     text_color="#7F7F7F").pack()

        corpo_info = ctk.CTkFrame(cartao_ingresso, fg_color="transparent")
        corpo_info.pack(padx=25, pady=10, fill="both", expand=True)

        ctk.CTkLabel(corpo_info, text="CÓDIGO VENDAS: #CNK-2026", font=("Courier New", 13, "bold"),
                     text_color="#333333").pack(anchor="w", pady=4)
        ctk.CTkLabel(corpo_info, text=f"FILME:   {texto_filme.upper()}", font=("Courier New", 14, "bold"),
                     text_color="#000000").pack(anchor="w", pady=6)
        ctk.CTkLabel(corpo_info, text=f"SESSÃO:  {texto_sessao}", font=("Courier New", 13), text_color="#1B1717").pack(
            anchor="w", pady=4)
        ctk.CTkLabel(corpo_info, text=f"TIPO:    {combo_ingresso.get().upper()}", font=("Courier New", 13),
                     text_color="#1B1717").pack(anchor="w", pady=4)
        ctk.CTkLabel(corpo_info, text=f"ASSENTO: Poltrona(s) {texto_assentos}", font=("Courier New", 13, "bold"),
                     text_color="#810000").pack(anchor="w", pady=6)

        ctk.CTkLabel(cartao_ingresso, text="-----------------------------------", font=("Courier New", 12),
                     text_color="#7F7F7F").pack()
        ctk.CTkLabel(cartao_ingresso, text=f"VALOR TOTAL:  {texto_total}", font=("Courier New", 16, "bold"),
                     text_color="#000000").pack(pady=10)

        ctk.CTkLabel(cartao_ingresso, text="||||| | |||| ||| || |||| | |||||", font=("Courier New", 18, "bold"),
                     text_color="#000000").pack(pady=(5, 0))
        ctk.CTkLabel(cartao_ingresso, text="MUITO OBRIGADO - BOM FILME!", font=("Courier New", 11, "italic"),
                     text_color="#555555").pack(pady=(0, 15))

        def acao_fechar_modal():
            modal.destroy()
            alternar_sessao_e_construir_mapa()

        btn_fechar = ctk.CTkButton(modal, text="Concluir Impressão", width=200, height=45, fg_color="#5C1010",
                                   hover_color="#3D0B0B", font=("Helvetica", 14, "bold"), command=acao_fechar_modal)
        btn_fechar.pack(pady=(0, 20))

    # COMPONENTES DE INTERAÇÃO
    combo_filme = ctk.CTkComboBox(left_panel, width=300, height=45, fg_color="#D5D1C3", text_color="#000000",
                                  dropdown_fg_color="#D5D1C3", dropdown_text_color="#000000", font=("Helvetica", 14),
                                  values=["Selecione o Filme"], command=atualizar_combo_sessoes)
    combo_filme.pack(pady=(0, 20))

    combo_sessao = ctk.CTkComboBox(left_panel, width=300, height=45, fg_color="#D5D1C3", text_color="#000000",
                                   dropdown_fg_color="#D5D1C3", dropdown_text_color="#000000", font=("Helvetica", 14),
                                   values=["Selecione a Sessão"], command=alternar_sessao_e_construir_mapa)
    combo_sessao.pack(pady=(0, 20))

    combo_ingresso = ctk.CTkComboBox(left_panel, width=300, height=45, fg_color="#D5D1C3", text_color="#000000",
                                     dropdown_fg_color="#D5D1C3", dropdown_text_color="#000000", font=("Helvetica", 14),
                                     values=["Inteira", "Meia-Entrada (Estudante)"], command=atualizar_resumo_venda)
    combo_ingresso.pack(pady=(0, 40))

    label_assento = ctk.CTkLabel(left_panel, text="Assento Selecionado: --", font=("Helvetica", 16),
                                 text_color="#FFFFFF")
    label_assento.pack(anchor="w", padx=25, pady=5)

    label_total = ctk.CTkLabel(left_panel, text="Total a Pagar: R$ 0,00", font=("Helvetica", 20, "bold"),
                               text_color="#FFFFFF")
    label_total.pack(anchor="w", padx=25, pady=(5, 40))

    # PAINEL DIREITO (Layout da Sala)
    right_panel = ctk.CTkFrame(app, fg_color="transparent")
    right_panel.pack(side="right", fill="both", expand=True)

    tela_cinema = ctk.CTkLabel(right_panel, text="TELA", font=("Helvetica", 16, "bold"), fg_color="#D5D1C3",
                               text_color="#000000", width=600, height=30, corner_radius=10)
    tela_cinema.pack(pady=(40, 20))

    matriz_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
    matriz_frame.pack(anchor="n", pady=(10, 0))

    def clicar_poltrona(fileira, assento, botao):
        num_poltrona = (fileira * 8) + assento + 1
        nome_assento = str(num_poltrona)

        if botao.cget("fg_color") == "#810000":
            return

        if botao.cget("fg_color") == "#869B7E":
            botao.configure(fg_color="#EEEBDD", text_color="#1B1717", hover_color="#1B1717")
            if nome_assento in assentos_selecionados:
                assentos_selecionados.remove(nome_assento)
        else:
            botao.configure(fg_color="#869B7E", text_color="#1B1717", hover_color="#6B7C64")
            assentos_selecionados.append(nome_assento)

        if assentos_selecionados:
            assentos_ordenados = sorted(assentos_selecionados, key=int)
            label_assento.configure(text=f"Poltronas: {', '.join(assentos_ordenados)}")
        else:
            label_assento.configure(text="Assento Selecionado: --")

        atualizar_resumo_venda()

    # TRAVA CONTRA DUPLICIDADE: Copia e limpa imediatamente no início da execução
    def finalizar_venda_db():
        if not assentos_selecionados:
            label_total.configure(text="Selecione os assentos!", text_color="#FF3333")
            return

        # Isola e limpa os assentos globais na mesma hora!
        assentos_para_este_bilhete = assentos_selecionados.copy()
        assentos_selecionados.clear()

        if id_sessao_atual is not None:
            try:
                conexao = sqlite3.connect('banco.db')
                cursor = conexao.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")

                for assento in assentos_para_este_bilhete:
                    cursor.execute("INSERT INTO tickets (session_id, seat_code) VALUES (?, ?)",
                                   (id_sessao_atual, assento))

                conexao.commit()
                conexao.close()
            except Exception as e:
                label_total.configure(text="Erro ao salvar no Banco!", text_color="#FF3333")
                print(f"Erro crítico no SQLite: {e}")
                return

        else:
            print("Aviso: Gerando bilhete simulado (modo homologação).")

        # Abre o bilhete passando a cópia segura e única
        abrir_modal_bilhete(assentos_para_este_bilhete)

    btn_finalizar = ctk.CTkButton(left_panel, text="FINALIZAR VENDA", width=300, height=60, corner_radius=15,
                                  fg_color="#5C1010", hover_color="#3D0B0B", font=("Helvetica", 18, "bold"),
                                  text_color="#FFFFFF", command=finalizar_venda_db)
    btn_finalizar.pack(side="bottom", pady=40)

    # Inicialização automática controlada
    garantir_tabela_ingressos()
    carregar_filmes_no_combo()
    alternar_sessao_e_construir_mapa()

    app.mainloop()


if __name__ == "__main__":
    abrir_atendimento()