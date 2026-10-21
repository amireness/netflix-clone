
from multiprocessing.dummy import connection
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL UNIQUE,
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        )
    """)

    cursor.execute("PRAGMA table_info(movies)")
    columns = [column[1] for column in cursor.fetchall()]

    if "release_year" not in columns:
        cursor.execute(
            "ALTER TABLE movies ADD COLUMN release_year INTEGER"
        )

    if "description" not in columns:
        cursor.execute(
            "ALTER TABLE movies ADD COLUMN description TEXT"
        )

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

    movie_details = [
        (2010, "A thief enters people's dreams to steal secrets.", 1),
        (2014, "A team travels through space to find a new home for humanity.", 2),
        (2008, "Batman faces the Joker as chaos spreads through Gotham.", 3),
        (1999, "A hacker discovers the truth about his reality.", 4),
        (2021, "A young man becomes involved in a struggle for control of Arrakis.", 5),
        (2014, "A retired assassin returns to the criminal underworld.", 6),
        (2015, "Survivors escape across a desert in a high-speed chase.", 7),
        (1994, "Two prisoners form a friendship over many years.", 8),
        (1994, "A man experiences major moments in American history.", 9),
        (2010, "The story of the founding of a major social network.", 10),
        (2014, "A hotel concierge becomes involved in a mysterious crime.", 11),
        (2007, "Two friends try to make the most of their final days of high school.", 12),
        (2019, "A detective investigates the death of a wealthy novelist.", 13),
        (2006, "Two rival magicians compete to create the ultimate illusion.", 14),
        (2001, "A group of thieves plans an elaborate Las Vegas casino heist.", 15),
    ]

    cursor.executemany("""
        UPDATE movies
        SET release_year = ?, description = ?
        WHERE id = ?
    """, movie_details)
    
    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()
    print("Movie database initialized and populated!")
