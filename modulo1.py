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
