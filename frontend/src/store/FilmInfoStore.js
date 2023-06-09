import { makeAutoObservable, runInAction } from "mobx";
import { Movie } from './Movie.js';

class FilmInfoStore {
    movies = [];
    currentMovieIndex = 0;

    constructor() {
        makeAutoObservable(this);
        this.loadFromLocalStorage();
    }

    loadFromLocalStorage() {
        const moviesJson = localStorage.getItem('movies');
        if (moviesJson) {
            this.movies = JSON.parse(moviesJson).map(movieJson => new Movie(movieJson));

        }
        const currentMovieIndex = localStorage.getItem('currentMovieIndex');
        if (currentMovieIndex) {
            this.currentMovieIndex = Number(currentMovieIndex);

        }
    }

    saveToLocalStorage() {
        localStorage.setItem('movies', JSON.stringify(this.movies));
        localStorage.setItem('currentMovieIndex', this.currentMovieIndex);
    }

    async fetchMovies() {
        const response = await fetch('/example.json');
        const moviesJson = await response.json();
        this.movies = moviesJson.map(movieJson => new Movie(movieJson));
        this.saveToLocalStorage();
    }

    loadMovies(data) {
        runInAction(() => {
            this.currentMovieIndex = 0;
            filmInfoStore.movies = data.map(movieJson => new Movie(movieJson));
            this.saveToLocalStorage();
        });
    }

    setCurrentMovieIndex(index) {
        this.currentMovieIndex = index;
        this.saveToLocalStorage();
    }

    increaseCurrentMovieIndex() {
        if (this.currentMovieIndex < this.movies.length - 1) {
            this.currentMovieIndex++;
            this.saveToLocalStorage();
        }
    }

    decreaseCurrentMovieIndex() {
        if (this.currentMovieIndex > 0) {
            this.currentMovieIndex--;
            this.saveToLocalStorage();
        }
    }

    clearLocalStorage() {
        localStorage.removeItem('movies');
        localStorage.removeItem('currentMovieIndex');
    }

    redirectKinopoisk() {
        if (this.currentMovie && this.currentMovie.link) {
            window.open(this.currentMovie.link, '_blank');
        }
    }

    redirectYouTube() {
        if (this.currentMovie && this.currentMovie.trailer && this.currentMovie.trailer.url) {
            window.open(this.currentMovie.trailer.url, '_blank');
        }
    }

    get currentMovie() {
        return this.movies[this.currentMovieIndex];
    }

    get currentMovieSimilarMovies() {
        return this.currentMovie && this.currentMovie.similarMovies ? this.currentMovie.similarMovies : [];
    }
}

export const filmInfoStore = new FilmInfoStore();

