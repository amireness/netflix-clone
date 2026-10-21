import sqlite3

import pytest

import app as movie_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    database = tmp_path / "test_movies.db"

    connection = sqlite3.connect(database)
    connection.execute("""
        CREATE TABLE movies (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            release_year INTEGER,
            description TEXT
        )
    """)

    connection.execute("""
        CREATE TABLE watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL UNIQUE,
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        )
    """)

    connection.executemany(
        """
        INSERT INTO movies
        (id, title, genre, release_year, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (1, "Inception", "Sci-Fi", 2010,
            "A thief enters people's dreams to steal secrets."),
            (2, "Interstellar", "Sci-Fi", 2014,
            "A team travels through space to find a new home for humanity."),
            (3, "The Dark Knight", "Action", 2008,
            "Batman faces the Joker as chaos spreads through Gotham."),
        ],
    )

    connection.commit()
    connection.close()

    monkeypatch.setattr(movie_app, "DATABASE", str(database))

    movie_app.app.config["TESTING"] = True

    with movie_app.app.test_client() as test_client:
        yield test_client


def test_get_all_movies(client):
    response = client.get("/api/movies")

    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_search_by_title(client):
    response = client.get("/api/movies?search=Inter")

    movies = response.get_json()

    assert response.status_code == 200
    assert len(movies) == 1
    assert movies[0]["title"] == "Interstellar"


def test_filter_by_genre(client):
    response = client.get("/api/movies?genre=Sci-Fi")

    movies = response.get_json()

    assert response.status_code == 200
    assert len(movies) == 2


def test_combined_filters(client):
    response = client.get(
        "/api/movies?search=Inception&genre=Action"
    )

    assert response.status_code == 200
    assert response.get_json() == []


def test_no_matching_movies(client):
    response = client.get("/api/movies?search=Avatar")

    assert response.status_code == 200
    assert response.get_json() == []

def test_movie_details(client):
    response = client.get("/api/movies?search=Inception")

    assert response.status_code == 200

    movie = response.get_json()[0]

    assert movie["title"] == "Inception"
    assert movie["release_year"] == 2010
    assert movie["description"] == (
        "A thief enters people's dreams to steal secrets."
    )

def test_empty_watchlist(client):
    response = client.get("/api/watchlist")

    assert response.status_code == 200
    assert response.get_json() == []


def test_add_movie_to_watchlist(client):
    response = client.post(
        "/api/watchlist",
        json={"movie_id": 1}
    )

    assert response.status_code == 201

    watchlist = client.get("/api/watchlist").get_json()

    assert len(watchlist) == 1
    assert watchlist[0]["title"] == "Inception"


def test_prevent_duplicate_watchlist_movies(client):
    client.post("/api/watchlist", json={"movie_id": 1})

    response = client.post(
        "/api/watchlist",
        json={"movie_id": 1}
    )

    assert response.status_code == 409

    watchlist = client.get("/api/watchlist").get_json()
    assert len(watchlist) == 1


def test_remove_movie_from_watchlist(client):
    client.post("/api/watchlist", json={"movie_id": 1})

    response = client.delete("/api/watchlist/1")

    assert response.status_code == 200
    assert client.get("/api/watchlist").get_json() == []