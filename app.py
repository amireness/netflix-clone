import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

DATABASE = "movies.db"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/movies")
def get_movies():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    search = request.args.get("search", "").strip()
    genre = request.args.get("genre", "").strip()

    query = "SELECT * FROM movies WHERE 1=1"
    parameters = []

    if search:
        query += " AND title LIKE ?"
        parameters.append(f"%{search}%")

    if genre:
        query += " AND genre = ? COLLATE NOCASE"
        parameters.append(genre)

    cursor.execute(query, parameters)

    movies = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return jsonify(movies)

@app.route("/api/watchlist", methods=["GET"])
def get_watchlist():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    movies = connection.execute("""
        SELECT movies.*
        FROM watchlist
        JOIN movies ON watchlist.movie_id = movies.id
        ORDER BY watchlist.id
    """).fetchall()

    connection.close()

    return jsonify([dict(movie) for movie in movies])

@app.route("/api/watchlist", methods=["POST"])
def add_to_watchlist():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or type(data.get("movie_id")) is not int:
        return jsonify({"error": "A valid movie_id is required"}), 400

    movie_id = data["movie_id"]

    connection = sqlite3.connect(DATABASE)
    connection.execute("PRAGMA foreign_keys = ON")

    movie = connection.execute(
        "SELECT id FROM movies WHERE id = ?",
        (movie_id,)
    ).fetchone()

    if movie is None:
        connection.close()
        return jsonify({"error": "Movie not found"}), 404

    try:
        connection.execute(
            "INSERT INTO watchlist (movie_id) VALUES (?)",
            (movie_id,)
        )
        connection.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Movie already in watchlist"}), 409
    finally:
        connection.close()

    return jsonify({"message": "Movie added to watchlist"}), 201

@app.route("/api/watchlist/<int:movie_id>", methods=["DELETE"])
def remove_from_watchlist(movie_id):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.execute(
        "DELETE FROM watchlist WHERE movie_id = ?",
        (movie_id,)
    )

    connection.commit()
    deleted = cursor.rowcount
    connection.close()

    if deleted == 0:
        return jsonify({"error": "Movie not in watchlist"}), 404

    return jsonify({"message": "Movie removed from watchlist"})

if __name__ == "__main__":
    app.run(debug=True)
