import sqlite3


def setup_db_modulo2():
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Cria a Tabela de Sessões
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

def criar_tabela_ingressos():
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            seat_code TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions (id_session)
        )
    """)

    connection.commit()
    connection.close()


def list_movies_summary():
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, title FROM movies')
    movies = cursor.fetchall()
    connection.close()
    
    print('\n\t--- FILMES DISPONÍVEIS ---')
    for m in movies:
        print(f"ID: {m[0]} | Título: {m[1]}")

def list_screens_summary():
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()
    cursor.execute('SELECT screen_number, screen_type FROM screens')
    screens = cursor.fetchall()
    connection.close()
    
    print('\n\t--- SALAS DISPONÍVEIS ---')
    for s in screens:
        print(f"Sala Número: {s[0]} | Tipo: {s[1]}")

def register_session_db(movie_id, screen_number, session_time, base_price):
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