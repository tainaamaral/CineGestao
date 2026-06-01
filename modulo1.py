import sqlite3

def setup_db():
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies ( 
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT NOT NULL,
                duration INTEGER NOT NULL,
                age_rating TEXT NOT NULL,
                synopsis TEXT NOT NULL
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS screens (
                screen_number INTEGER NOT NULL PRIMARY KEY,
                rows_qty INTEGER NOT NULL,
                sits_per_row INTEGER NOT NULL,
                total_capacity INTEGER NOT NULL,
                screen_type TEXT NOT NULL
            )
        """)

    connection.commit()
    connection.close()

def register_movies(title, genre, duration, age_rating, synopsis):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()
    cursor.execute(""" INSERT INTO movies (title, genre, duration, age_rating, synopsis) 
        VALUES (?, ?, ?, ?, ?)
        
    """ , (title, genre, duration, age_rating, synopsis))

    connection.commit()
    connection.close()
    print('Filme cadastrado com sucesso!!')

def register_screens(screen_number, rows_qty, sits_per_row, screen_type):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    total_capacity = rows_qty * sits_per_row
    cursor.execute(""" 
    INSERT INTO screens (screen_number, rows_qty, sits_per_row, total_capacity, screen_type) 
    VALUES (?, ?, ?, ?, ?)
    """ , (screen_number, rows_qty, sits_per_row, total_capacity, screen_type))

    connection.commit()
    connection.close()
    print('Sala cadastrada com sucesso!!')

setup_db()


def list_movies():
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM movies')
    all_movies = cursor.fetchall()

    print('\n \t --- LISTA DE FILMES ---')
    for movie in all_movies:
        print(f''' ID: {movie[0]} | Título: {movie[1]} | Gênero: {movie[2]} | 
        Duração: {movie[3]}min. | Classificação Indicativa: {movie[4]}+ | Sinopse: {movie[5]} ''')

    connection.close()

def list_screens():
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM screens')
    all_screens = cursor.fetchall()

    print('\n \t --- SALAS DE FILMES ---')
    for screen in all_screens:
        print(f''' Número da Sala: {screen[0]} | Quantidade de Fileiras: {screen[1]} | 
        Assentos por Fileira: {screen[2]} | Capacidade Total: {screen[3]} | Tipo de Tela: {screen[4]} ''')

list_movies()
list_screens()



