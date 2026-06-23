import customtkinter as ctk
import sqlite3
import modulo1
import modulo2


def abrir_dashboard():
    ctk.set_appearance_mode("dark")
    modulo2.setup_db_modulo2()

    app = ctk.CTk()
    app.geometry("1280x720")
    app.title("CineGestão - Administração")
    app.configure(fg_color="#1A1A1A")

    top_frame = ctk.CTkFrame(app, height=60, fg_color="#000000", corner_radius=0)
    top_frame.pack(side="top", fill="x")

    def voltar_para_inicio():
        app.destroy()
        import main
        main.iniciar_sistema()

    btn_voltar = ctk.CTkButton(top_frame, text="⬅ Voltar", width=90, height=35, fg_color="#242424",
                               hover_color="#333333", font=("Helvetica", 13, "bold"), command=voltar_para_inicio)
    btn_voltar.pack(side="left", padx=15, pady=12)

    titulo_topo = ctk.CTkLabel(top_frame, text="CINEGESTÃO - PAINEL ADMINISTRATIVO", font=("Helvetica", 20, "bold"),
                               text_color="#FFFFFF")
    titulo_topo.pack(pady=15, expand=True)

    # LÓGICA DE NAVEGAÇÃO E ATUALIZAÇÃO DAS LISTAS
    def selecionar_aba(aba_nome):
        frame_filmes.pack_forget()
        frame_salas.pack_forget()
        frame_sessoes.pack_forget()

        btn_filmes.configure(fg_color="transparent", text_color="#A0A0A0")
        btn_salas.configure(fg_color="transparent", text_color="#A0A0A0")
        btn_sessoes.configure(fg_color="transparent", text_color="#A0A0A0")

        if aba_nome == "filmes":
            frame_filmes.pack(fill="both", expand=True)
            btn_filmes.configure(fg_color="#810000", text_color="#FFFFFF")
            atualizar_lista_filmes()
        elif aba_nome == "salas":
            frame_salas.pack(fill="both", expand=True)
            btn_salas.configure(fg_color="#810000", text_color="#FFFFFF")
            atualizar_lista_salas()
        elif aba_nome == "sessoes":
            frame_sessoes.pack(fill="both", expand=True)
            btn_sessoes.configure(fg_color="#810000", text_color="#FFFFFF")
            carregar_dados_reais_nas_sessoes()
            atualizar_lista_sessoes()

    # MENU LATERAL (SIDEBAR)
    sidebar = ctk.CTkFrame(app, width=250, fg_color="#121212", corner_radius=0)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    titulo_sidebar = ctk.CTkLabel(sidebar, text="MENU", font=("Helvetica", 18, "bold"), text_color="#7F7F7F")
    titulo_sidebar.pack(pady=(20, 20))

    btn_filmes = ctk.CTkButton(sidebar, text="🎬 Filmes", font=("Helvetica", 16, "bold"), anchor="w", height=45,
                               hover_color="#630000", command=lambda: selecionar_aba("filmes"))
    btn_filmes.pack(fill="x", padx=15, pady=5)

    btn_salas = ctk.CTkButton(sidebar, text="🏢 Salas", font=("Helvetica", 16), text_color="#A0A0A0", anchor="w",
                              height=45, hover_color="#242424", command=lambda: selecionar_aba("salas"))
    btn_salas.pack(fill="x", padx=15, pady=5)

    btn_sessoes = ctk.CTkButton(sidebar, text="📅 Sessões", font=("Helvetica", 16), text_color="#A0A0A0", anchor="w",
                                height=45, hover_color="#242424", command=lambda: selecionar_aba("sessoes"))
    btn_sessoes.pack(fill="x", padx=15, pady=5)

    btn_voltar_menu = ctk.CTkButton(sidebar, text="⬅ Voltar ao Menu", font=("Helvetica", 15, "bold"),
                                    fg_color="#242424", hover_color="#333333", height=45, command=voltar_para_inicio)
    btn_voltar_menu.pack(side="bottom", fill="x", padx=15, pady=25)

    # ÁREA CENTRAL
    conteudo_frame = ctk.CTkFrame(app, fg_color="transparent")
    conteudo_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # ==========================================
    # TELA 1: FILMES
    # ==========================================
    frame_filmes = ctk.CTkFrame(conteudo_frame, fg_color="transparent")

    form_filmes = ctk.CTkFrame(frame_filmes, width=350, fg_color="#242424", corner_radius=15)
    form_filmes.pack(side="left", fill="y", padx=(0, 20))
    form_filmes.pack_propagate(False)

    ctk.CTkLabel(form_filmes, text="Cadastrar Novo Filme", font=("Helvetica", 20, "bold"), text_color="#FFFFFF").pack(
        pady=(25, 20))

    entrada_titulo = ctk.CTkEntry(form_filmes, placeholder_text="Título do Filme", width=300, height=40,
                                  fg_color="#EEEBDD", text_color="#000000")
    entrada_titulo.pack(pady=10)

    combo_genero = ctk.CTkComboBox(form_filmes,
                                   values=["Ação", "Comédia", "Drama", "Ficção Científica", "Terror", "Romance"],
                                   width=300, height=40, fg_color="#EEEBDD", text_color="#000000",
                                   dropdown_fg_color="#EEEBDD", dropdown_text_color="#000000")
    combo_genero.set("Selecione o Gênero")
    combo_genero.pack(pady=10)

    entrada_duracao = ctk.CTkEntry(form_filmes, placeholder_text="Duração (min)", width=300, height=40,
                                   fg_color="#EEEBDD", text_color="#000000")
    entrada_duracao.pack(pady=10)

    combo_classificacao = ctk.CTkComboBox(form_filmes,
                                          values=["Livre", "10 Anos", "12 Anos", "14 Anos", "16 Anos", "18 Anos"],
                                          width=300, height=40, fg_color="#EEEBDD", text_color="#000000",
                                          dropdown_fg_color="#EEEBDD", dropdown_text_color="#000000")
    combo_classificacao.set("Classificação Indicativa")
    combo_classificacao.pack(pady=10)

    entrada_sinopse = ctk.CTkEntry(form_filmes, placeholder_text="Breve Sinopse...", width=300, height=40,
                                   fg_color="#EEEBDD", text_color="#000000")
    entrada_sinopse.pack(pady=10)

    def comando_salvar_filme():
        try:
            title = entrada_titulo.get()
            genre = combo_genero.get()
            duration = int(entrada_duracao.get())
            age_rating = combo_classificacao.get()
            synopsis = entrada_sinopse.get()

            modulo1.register_movies(title, genre, duration, age_rating, synopsis)

            entrada_titulo.delete(0, 'end')
            entrada_duracao.delete(0, 'end')
            entrada_sinopse.delete(0, 'end')
            atualizar_lista_filmes()  # Atualiza a lista instantaneamente após salvar
        except ValueError:
            print("Erro: A duração do filme deve ser um número inteiro.")

    btn_salvar_filme = ctk.CTkButton(form_filmes, text="SALVAR FILME", font=("Helvetica", 16, "bold"),
                                     fg_color="#810000", hover_color="#630000", width=300, height=50, corner_radius=10,
                                     command=comando_salvar_filme)
    btn_salvar_filme.pack(side="bottom", pady=30)

    # Lado Direito: Catálogo de Filmes com Scroll
    lista_filmes = ctk.CTkScrollableFrame(frame_filmes, fg_color="#242424", corner_radius=15)
    lista_filmes.pack(side="right", fill="both", expand=True)
    ctk.CTkLabel(lista_filmes, text="Catálogo de Filmes", font=("Helvetica", 20, "bold"), text_color="#FFFFFF").pack(
        anchor="w", padx=15, pady=(10, 15))

    def atualizar_lista_filmes():
        # Limpa os itens antigos (ignorando o título)
        for widget in lista_filmes.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()
        try:
            conexao = sqlite3.connect('banco.db')
            cursor = conexao.cursor()
            cursor.execute("SELECT id, title, genre, duration FROM movies")
            filmes = cursor.fetchall()
            conexao.close()

            for filme in filmes:
                card = ctk.CTkFrame(lista_filmes, fg_color="#333333", corner_radius=8)
                card.pack(fill="x", padx=15, pady=5)
                ctk.CTkLabel(card, text=f"ID {filme[0]} | {filme[1].upper()}", font=("Helvetica", 14, "bold"),
                             text_color="#FFFFFF").pack(anchor="w", padx=15, pady=(8, 0))
                ctk.CTkLabel(card, text=f"{filme[2]} • {filme[3]} minutos", font=("Helvetica", 12),
                             text_color="#A0A0A0").pack(anchor="w", padx=15, pady=(0, 8))
        except Exception as e:
            print("Aviso na lista de filmes:", e)

    # ==========================================
    # TELA 2: SALAS
    # ==========================================
    frame_salas = ctk.CTkFrame(conteudo_frame, fg_color="transparent")

    form_salas = ctk.CTkFrame(frame_salas, width=350, fg_color="#242424", corner_radius=15)
    form_salas.pack(side="left", fill="y", padx=(0, 20))
    form_salas.pack_propagate(False)

    ctk.CTkLabel(form_salas, text="Cadastrar Nova Sala", font=("Helvetica", 20, "bold"), text_color="#FFFFFF").pack(
        pady=(25, 20))

    entrada_sala_num = ctk.CTkEntry(form_salas, placeholder_text="Número da Sala", width=300, height=40,
                                    fg_color="#EEEBDD", text_color="#000000")
    entrada_sala_num.pack(pady=10)
    entrada_fileiras = ctk.CTkEntry(form_salas, placeholder_text="Quantidade de Fileiras", width=300, height=40,
                                    fg_color="#EEEBDD", text_color="#000000")
    entrada_fileiras.pack(pady=10)
    entrada_assentos = ctk.CTkEntry(form_salas, placeholder_text="Assentos por Fileira", width=300, height=40,
                                    fg_color="#EEEBDD", text_color="#000000")
    entrada_assentos.pack(pady=10)

    combo_tipo_sala = ctk.CTkComboBox(form_salas, values=["Padrão", "IMAX", "3D", "VIP"], width=300, height=40,
                                      fg_color="#EEEBDD", text_color="#000000", dropdown_fg_color="#EEEBDD",
                                      dropdown_text_color="#000000")
    combo_tipo_sala.set("Tipo de Tela")
    combo_tipo_sala.pack(pady=10)

    def comando_salvar_sala():
        try:
            num = int(entrada_sala_num.get())
            rows = int(entrada_fileiras.get())
            sits = int(entrada_assentos.get())
            stype = combo_tipo_sala.get()

            total_capacity = rows * sits
            modulo1.register_screens(num, rows, sits, total_capacity, stype)

            entrada_sala_num.delete(0, 'end')
            entrada_fileiras.delete(0, 'end')
            entrada_assentos.delete(0, 'end')
            atualizar_lista_salas()
        except ValueError:
            print("Erro: Número, Fileiras e Assentos devem ser valores numéricos.")

    ctk.CTkButton(form_salas, text="SALVAR SALA", font=("Helvetica", 16, "bold"), fg_color="#810000",
                  hover_color="#630000", width=300, height=50, corner_radius=10, command=comando_salvar_sala).pack(
        side="bottom", pady=30)

    # Lado Direito: Catálogo de Salas com Scroll
    lista_salas = ctk.CTkScrollableFrame(frame_salas, fg_color="#242424", corner_radius=15)
    lista_salas.pack(side="right", fill="both", expand=True)
    ctk.CTkLabel(lista_salas, text="Salas Cadastradas", font=("Helvetica", 20, "bold"), text_color="#FFFFFF").pack(
        anchor="w", padx=15, pady=(10, 15))

    def atualizar_lista_salas():
        for widget in lista_salas.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()
        try:
            conexao = sqlite3.connect('banco.db')
            cursor = conexao.cursor()
            cursor.execute("SELECT screen_number, screen_type, total_capacity FROM screens")
            salas = cursor.fetchall()
            conexao.close()

            for sala in salas:
                card = ctk.CTkFrame(lista_salas, fg_color="#333333", corner_radius=8)
                card.pack(fill="x", padx=15, pady=5)
                ctk.CTkLabel(card, text=f"Sala {sala[0]} - {sala[1].upper()}", font=("Helvetica", 14, "bold"),
                             text_color="#FFFFFF").pack(anchor="w", padx=15, pady=(8, 0))
                ctk.CTkLabel(card, text=f"Capacidade: {sala[2]} lugares", font=("Helvetica", 12),
                             text_color="#A0A0A0").pack(anchor="w", padx=15, pady=(0, 8))
        except Exception as e:
            print("Aviso na lista de salas:", e)

    # ==========================================
    # TELA 3: SESSÕES
    # ==========================================
    frame_sessoes = ctk.CTkFrame(conteudo_frame, fg_color="transparent")

    form_sessoes = ctk.CTkFrame(frame_sessoes, width=350, fg_color="#242424", corner_radius=15)
    form_sessoes.pack(side="left", fill="y", padx=(0, 20))
    form_sessoes.pack_propagate(False)

    ctk.CTkLabel(form_sessoes, text="Agendar Sessão", font=("Helvetica", 20, "bold"), text_color="#FFFFFF").pack(
        pady=(25, 20))

    combo_filme_sessao = ctk.CTkComboBox(form_sessoes, values=["Carregando..."], width=300, height=40,
                                         fg_color="#EEEBDD", text_color="#000000", dropdown_fg_color="#EEEBDD",
                                         dropdown_text_color="#000000")
    combo_filme_sessao.set("ID do Filme")
    combo_filme_sessao.pack(pady=10)

    combo_sala_sessao = ctk.CTkComboBox(form_sessoes, values=["Carregando..."], width=300, height=40,
                                        fg_color="#EEEBDD", text_color="#000000", dropdown_fg_color="#EEEBDD",
                                        dropdown_text_color="#000000")
    combo_sala_sessao.set("Número da Sala")
    combo_sala_sessao.pack(pady=10)

    entrada_horario = ctk.CTkEntry(form_sessoes, placeholder_text="Horário (ex: 19:30)", width=300, height=40,
                                   fg_color="#EEEBDD", text_color="#000000")
    entrada_horario.pack(pady=10)

    entrada_preco = ctk.CTkEntry(form_sessoes, placeholder_text="Preço Base (ex: 30.50)", width=300, height=40,
                                 fg_color="#EEEBDD", text_color="#000000")
    entrada_preco.pack(pady=10)

    def carregar_dados_reais_nas_sessoes():
        try:
            conexao = sqlite3.connect('banco.db')
            cursor = conexao.cursor()

            cursor.execute("SELECT id, title FROM movies")
            filmes = cursor.fetchall()
            lista_filmes = [f"{f[0]} - {f[1]}" for f in filmes]
            if lista_filmes:
                combo_filme_sessao.configure(values=lista_filmes)
                combo_filme_sessao.set(lista_filmes[0])

            cursor.execute("SELECT screen_number FROM screens")
            salas = cursor.fetchall()
            lista_salas = [str(s[0]) for s in salas]
            if lista_salas:
                combo_sala_sessao.configure(values=lista_salas)
                combo_sala_sessao.set(lista_salas[0])

            conexao.close()
        except sqlite3.OperationalError:
            pass

    def comando_salvar_sessao():
        try:
            texto_filme = combo_filme_sessao.get()
            id_filme = int(texto_filme.split(" - ")[0])

            num_sala = int(combo_sala_sessao.get())
            horario = entrada_horario.get()
            preco = float(entrada_preco.get())

            modulo2.register_session_db(id_filme, num_sala, horario, preco)

            entrada_horario.delete(0, 'end')
            entrada_preco.delete(0, 'end')
            atualizar_lista_sessoes()
        except (ValueError, IndexError):
            print("Erro: Verifique os campos de horário e preço.")

    btn_salvar_sessao = ctk.CTkButton(form_sessoes, text="AGENDAR SESSÃO", font=("Helvetica", 16, "bold"),
                                      fg_color="#810000", hover_color="#630000", command=comando_salvar_sessao,
                                      width=300, height=50, corner_radius=10)
    btn_salvar_sessao.pack(side="bottom", pady=30)

    # Lado Direito: Grade de Sessões com Scroll
    lista_sessoes = ctk.CTkScrollableFrame(frame_sessoes, fg_color="#242424", corner_radius=15)
    lista_sessoes.pack(side="right", fill="both", expand=True)
    ctk.CTkLabel(lista_sessoes, text="Grade Horária de Sessões", font=("Helvetica", 20, "bold"),
                 text_color="#FFFFFF").pack(anchor="w", padx=15, pady=(10, 15))

    def atualizar_lista_sessoes():
        for widget in lista_sessoes.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()
        try:
            conexao = sqlite3.connect('banco.db')
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT s.session_time, s.screen_number, m.title, s.base_price 
                FROM sessions s
                JOIN movies m ON s.movie_id = m.id
                ORDER BY s.session_time
            """)
            sessoes = cursor.fetchall()
            conexao.close()

            for sessao in sessoes:
                card = ctk.CTkFrame(lista_sessoes, fg_color="#333333", corner_radius=8)
                card.pack(fill="x", padx=15, pady=5)
                ctk.CTkLabel(card, text=f"{sessao[0]} | Sala {sessao[1]} - {sessao[2].upper()}",
                             font=("Helvetica", 14, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=15,
                                                                                        pady=(8, 0))
                ctk.CTkLabel(card, text=f"Preço Base: R$ {sessao[3]:.2f}", font=("Helvetica", 12),
                             text_color="#869B7E").pack(anchor="w", padx=15, pady=(0, 8))
        except Exception as e:
            print("Aviso na lista de sessões:", e)

    # INICIALIZAÇÃO
    selecionar_aba("filmes")
    app.mainloop()


if __name__ == "__main__":
    abrir_dashboard()