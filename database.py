
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
        (4, "The Matrix", "Sci-Fi"),
        (5, "Dune", "Sci-Fi"),
        (6, "John Wick", "Action"),
        (7, "Mad Max: Fury Road", "Action"),
        (8, "The Shawshank Redemption", "Drama"),
        (9, "Forrest Gump", "Drama"),
        (10, "The Social Network", "Drama"),
        (11, "The Grand Budapest Hotel", "Comedy"),
        (12, "Superbad", "Comedy"),
        (13, "Knives Out", "Mystery"),
        (14, "The Prestige", "Mystery"),
        (15, "Ocean's Eleven", "Crime"),
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
