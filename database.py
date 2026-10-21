
import sqlite3

DATABASE = "movies.db"


def init_db():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            genre TEXT NOT NULL
        )
    """)

    movies = [
        (1, "Inception", "Sci-Fi"),
        (2, "Interstellar", "Sci-Fi"),
        (3, "The Dark Knight", "Action"),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO movies (id, title, genre)
        VALUES (?, ?, ?)
    """, movies)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()
    print("Movie database initialized and populated!")
