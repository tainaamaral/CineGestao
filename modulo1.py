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

def register_screens(screen_number, rows_qty, sits_per_row, total_capacity, screen_type):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()
    try:
        cursor.execute(""" 
        INSERT INTO screens (screen_number, rows_qty, sits_per_row, total_capacity, screen_type) 
        VALUES (?, ?, ?, ?, ?)
        """ , (screen_number, rows_qty, sits_per_row, total_capacity, screen_type))
        connection.commit()
        print('Sala cadastrada com sucesso!!')
    except sqlite3.IntegrityError:
        print('Erro! O número desta sala já está cadastrado')
    finally:
        connection.close()

# setup_db()

# def register_movie():
#     print('\n \t --- CADASTRO DE NOVO FILME ---')
#     title = input('Digite o titulo do filme: ')
#     genre = input('Digite o gênero do filme: ')
#     try:
#         duration = int(input('Digite a duração do filme em minutos: '))
#         if duration <= 0:
#             print('Erro! A duração deve ser maior que zero: ')
#             return
#     except ValueError:
#         print('Apenas números são aceitos!!')
#         return
#     age_rating = input('Digite a classificação indicativa: ')
#     synopsis = input('Digite a sinopse do filme: ')
#     register_movies(title, genre, duration, age_rating, synopsis)


# def register_room():
#     print('\n \t --- CADASTRO DE NOVA SALA ----')
#     try:
#         screen_number = int(input('Digite o número da sala: '))
#         rows_qty = int(input('Digite a quantidade de fileiras: '))
#         sits_per_row = int(input('Digite a quantidade de assentos por fileira: '))
#         if screen_number <= 0 or rows_qty <= 0 or sits_per_row <= 0:
#             print('Erro! A quantidade deve ser maior que 0')
#             return
#     except ValueError:
#         print('Apenas números são aceitos!')
#         return
#     total_capacity = rows_qty * sits_per_row
#     screen_type = input('Digite o tipo de tela: ')
#     register_screens(screen_number, rows_qty, sits_per_row, total_capacity, screen_type)
#
# register_movie()
# register_room()

# def list_movies():
#     connection = sqlite3.connect('banco.db')
#     cursor = connection.cursor()
#
#     cursor.execute('SELECT * FROM movies')
#     all_movies = cursor.fetchall()
#
#     print('\n \t --- LISTA DE FILMES ---')
#     for movie in all_movies:
#         print(f''' ID: {movie[0]} | Título: {movie[1]} | Gênero: {movie[2]} |
#         Duração: {movie[3]}min. | Classificação Indicativa: {movie[4]}+ | Sinopse: {movie[5]} ''')
#
#     connection.close()
#
# def list_screens():
#     connection = sqlite3.connect('banco.db')
#     cursor = connection.cursor()
#     cursor.execute('SELECT * FROM screens')
#     all_screens = cursor.fetchall()
#
#     print('\n \t --- SALAS DE FILMES ---')
#     for screen in all_screens:
#         print(f''' Número da Sala: {screen[0]} | Quantidade de Fileiras: {screen[1]} |
#         Assentos por Fileira: {screen[2]} | Capacidade Total: {screen[3]} | Tipo de Tela: {screen[4]} ''')
#
# list_movies()
# list_screens()
