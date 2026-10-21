const searchInput = document.getElementById("search");
const genreSelect = document.getElementById("genre");
const movieList = document.getElementById("movie-list");
const watchlistMovies = document.getElementById("watchlist-movies");

async function loadMovies() {
    const search = searchInput.value.trim();
    const genre = genreSelect.value;

    const params = new URLSearchParams();

    if (search) {
        params.append("search", search);
    }

    if (genre) {
        params.append("genre", genre);
    }

    let movies;
    let savedMovieIds;

    try {
        const response = await fetch(`/api/movies?${params}`);

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        movies = await response.json();

        const watchlistResponse = await fetch("/api/watchlist");

        if (!watchlistResponse.ok) {
            throw new Error(`HTTP error: ${watchlistResponse.status}`);
        }

        const watchlist = await watchlistResponse.json();

        savedMovieIds = new Set(
            watchlist.map(movie => movie.id)
        );

    } catch (error) {
        console.error("Failed to load movies:", error);
        movieList.textContent = "Unable to load movies. Please try again.";
        return;
    }

    movieList.innerHTML = "";

    if (movies.length === 0) {
        movieList.textContent = "No movies found.";
        return;
    }

    movies.forEach(movie => {
        const card = document.createElement("div");
        card.className = "movie-card";

        const title = document.createElement("h3");
        title.textContent = movie.title;

        const details = document.createElement("p");
        details.className = "movie-details";
        details.textContent = `${movie.release_year} • ${movie.genre}`;

        const description = document.createElement("p");
        description.className = "movie-description";
        description.textContent = movie.description;

        const watchlistButton = document.createElement("button");

        const isSaved = savedMovieIds.has(movie.id);

        watchlistButton.className = "watchlist-button";
        watchlistButton.textContent = isSaved
            ? "✓ In My List"
            : "+ My List";

        watchlistButton.addEventListener("click", () => {
            toggleWatchlist(movie.id, isSaved);
        });

        card.appendChild(title);
        card.appendChild(details);
        card.appendChild(description);
        card.appendChild(watchlistButton);

        movieList.appendChild(card);
    });
}

async function toggleWatchlist(movieId, isSaved) {
    const url = isSaved
        ? `/api/watchlist/${movieId}`
        : "/api/watchlist";

    const options = isSaved
        ? { method: "DELETE" }
        : {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ movie_id: movieId })
        };

    try {
        const response = await fetch(url, options);

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        await loadMovies();
        await loadWatchlist();

    } catch (error) {
        console.error("Watchlist update failed:", error);
        alert("Unable to update your watchlist. Please try again.");
    }
}

searchInput.addEventListener("input", loadMovies);
genreSelect.addEventListener("change", loadMovies);

async function loadWatchlist() {
    try {
        const response = await fetch("/api/watchlist");

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const movies = await response.json();

        watchlistMovies.innerHTML = "";

        if (movies.length === 0) {
            watchlistMovies.textContent = "Your watchlist is empty.";
            return;
        }

        movies.forEach(movie => {
            const card = document.createElement("div");
            card.className = "movie-card";

            const title = document.createElement("h3");
            title.textContent = movie.title;

            const details = document.createElement("p");
            details.className = "movie-details";
            details.textContent = `${movie.release_year} • ${movie.genre}`;

            const description = document.createElement("p");
            description.className = "movie-description";
            description.textContent = movie.description;

            const removeButton = document.createElement("button");
            removeButton.className = "watchlist-button";
            removeButton.textContent = "Remove from My List";

            removeButton.addEventListener("click", () => {
                toggleWatchlist(movie.id, true);
            });

            card.appendChild(title);
            card.appendChild(details);
            card.appendChild(description);
            card.appendChild(removeButton);

            watchlistMovies.appendChild(card);
        });

    } catch (error) {
        console.error("Failed to load watchlist:", error);
        watchlistMovies.textContent = "Unable to load watchlist.";
    }
}

loadMovies();
loadWatchlist();