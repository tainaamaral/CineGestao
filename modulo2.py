import sqlite3

def setup_db_modulo2():
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id_session INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            screen_number INTEGER NOT NULL,
            session_time TEXT NOT NULL,         -- Formato 'HH:MM'
            base_price REAL NOT NULL,
            FOREIGN KEY (movie_id) REFERENCES movies (id),
            FOREIGN KEY (screen_number) REFERENCES screens (screen_number)
        )
    """)
    connection.commit()
    connection.close()

def list_movies_summary():
    """Versão simplificada de listagem para o administrador escolher o filme"""
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, title FROM movies')
    movies = cursor.fetchall()
    connection.close()
    
    print('\n\t--- FILMES DISPONÍVEIS ---')
    for m in movies:
        print(f"ID: {m[0]} | Título: {m[1]}")

def list_screens_summary():
    """Versão simplificada de listagem para o administrador escolher a sala"""
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()
    cursor.execute('SELECT screen_number, screen_type FROM screens')
    screens = cursor.fetchall()
    connection.close()
    
    print('\n\t--- SALAS DISPONÍVEIS ---')
    for s in screens:
        print(f"Sala Número: {s[0]} | Tipo: {s[1]}")

def register_session_db(movie_id, screen_number, session_time, base_price):
    """Insere a sessão no banco de dados com validação de Chave Estrangeira"""
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    try:
        cursor.execute(""" 
            INSERT INTO sessions (movie_id, screen_number, session_time, base_price) 
            VALUES (?, ?, ?, ?)
        """, (movie_id, screen_number, session_time, base_price))
        connection.commit()
        print('\nSessão agendada com sucesso!!')
    except sqlite3.IntegrityError:
        print('\nErro! O ID do filme ou o Número da sala digitado não existe.')
    finally:
        connection.close()

def register_session():
    """Interface de usuário para cadastrar a sessão"""
    print('\n\t--- AGENDAMENTO DE SESSÃO ---')
    

    list_movies_summary()
    list_screens_summary()
    print("-" * 40)
    
    try:
        movie_id = int(input('Digite o ID do filme: '))
        screen_number = int(input('Digite o número da sala: '))
        session_time = input('Digite o horário (ex: 19:30): ')
        base_price = float(input('Digite o preço base do ingresso (R$): '))
        
        if base_price <= 0:
            print('Erro! O preço deve ser maior que zero.')
            return
            
    except ValueError:
        print('Erro! Dados numéricos inválidos nos campos de ID, Sala ou Preço.')
        return

    register_session_db(movie_id, screen_number, session_time, base_price)

def list_schedule():
    """Exibe a grade horária completa trazendo os nomes usando INNER JOIN"""
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()
    
    query = """
        SELECT s.id_session, m.title, s.screen_number, s.session_time, s.base_price, m.duration
        FROM sessions s
        INNER JOIN movies m ON s.movie_id = m.id
        INNER JOIN screens sc ON s.screen_number = sc.screen_number
    """
    cursor.execute(query)
    all_sessions = cursor.fetchall()
    connection.close()

    print('\n\t--- GRADE HORÁRIA / SESSÕES CADASTRADAS ---')
    if not all_sessions:
        print("Nenhuma sessão agendada no momento.")
        return

    for session in all_sessions:
        print(f"ID Sessão: {session[0]} | Filme: {session[1]} ({session[5]}min) | Sala: {session[2]} | Horário: {session[3]} | Preço: R$ {session[4]:.2f}")

def delete_session():
    """Remove uma sessão da grade"""
    list_schedule()
    try:
        id_session = int(input('\nDigite o ID da sessão que deseja cancelar: '))
    except ValueError:
        print('ID inválido.')
        return

    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM sessions WHERE id_session = ?", (id_session,))
    
    if cursor.rowcount > 0:
        print('Sessão cancelada com sucesso!')
    else:
        print('Sessão não encontrada.')
        
    connection.commit()
    connection.close()

def menu_modulo2():
    """Menu principal do seu módulo"""
    setup_db_modulo2()
    while True:
        print('\n=== MÓDULO 2: PLANEJAMENTO DA GRADE HORÁRIA ===')
        print('1. Agendar Nova Sessão')
        print('2. Visualizar Grade Horária')
        print('3. Cancelar Sessão')
        print('0. Sair')
        
        opcao = input('Escolha uma opção: ')
        if opcao == '1':
            register_session()
        elif opcao == '2':
            list_schedule()
        elif opcao == '3':
            delete_session()
        elif opcao == '0':
            print("Saindo do Módulo 2...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_modulo2()