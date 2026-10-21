import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

DATABASE = "movies.db"


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


if __name__ == "__main__":
    app.run(debug=True)
