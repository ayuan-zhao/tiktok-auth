import sqlite3

def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE access_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
