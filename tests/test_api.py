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
            genre TEXT NOT NULL
        )
    """)

    connection.executemany(
        "INSERT INTO movies VALUES (?, ?, ?)",
        [
            (1, "Inception", "Sci-Fi"),
            (2, "Interstellar", "Sci-Fi"),
            (3, "The Dark Knight", "Action"),
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
