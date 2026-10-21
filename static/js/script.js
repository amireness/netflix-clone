const searchInput = document.getElementById("search");
const genreSelect = document.getElementById("genre");
const movieList = document.getElementById("movie-list");

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

    try {
        const response = await fetch(`/api/movies?${params}`);

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        movies = await response.json();

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

        const genre = document.createElement("p");
        genre.textContent = movie.genre;

        card.appendChild(title);
        card.appendChild(genre);
        movieList.appendChild(card);
    });
}

searchInput.addEventListener("input", loadMovies);
genreSelect.addEventListener("change", loadMovies);

loadMovies();
