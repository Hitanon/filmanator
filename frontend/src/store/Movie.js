export class Movie {
    constructor(json) {
        this.id = json.id;
        this.fees = json.fees;
        this.rating = json.rating;
        this.match_percentage = json.match_percentage;
        this.movieLength = json.movieLength;
        this.name = json.name;
        this.description = json.description;
        this.year = json.year;
        this.budget = json.budget;
        this.poster = json.poster;
        this.genres = json.genres;
        this.countries = json.countries;
        this.seasons_count = json.seasons_count;
        this.alternativeName = json.alternativeName;
        this.shortDescription = json.shortDescription;
        this.ageRating = json.ageRating;
        this.similarMovies = json.similarMovies;
        this.isSeries = json.isSeries;
        this.link = json.link;
        this.trailer = json.trailer;
        this.actors = json.actors;
        this.directors = json.directors;
    }

    get title() {
        return `${this.name} (${this.year})`;
    }

    get alternativeTitle() {
        return this.alternativeName;
    }

    get matchPercentage() {
        return `${this.match_percentage}%`;
    }

    set matchPercentage(value) {
        this.match_percentage = value;
    }

    get genresList() {
        if (this.genres) {
            return this.genres.map(genre => genre.name).join(', ');
        }
        return '';
    }

    get countriesList() {
        if (this.countries) {
            return this.countries.map(country => country.name).join(', ');
        }
        return '';
    }

    get actorsList() {
        if (this.actors) {
            return this.actors.join(',\n');
        }
        return '';
    }

    get directorsList() {
        if (this.directors) {
            return this.directors.join(', ');
        }
        return '';
    }

    get imdbRating() {
        if (this.rating){
            return this.rating.imdb.toFixed(1);
        }
        return '';
    }

    get kinopoiskRating() {
        if (this.rating){
            return this.rating.kp.toFixed(1);
        }
        return '';
    }

    get posterUrl() {
        if (this.poster){
            return this.poster.previewUrl;
        }
        return '';
    }

    get ageRatingString() {
        return `${this.ageRating}+`;
    }

    get trailerUrl() {
        if (this.trailer){
            return this.trailer.url;
        }
        return '';
    }

    get feesString() {
        if (this.fees) {
            const feesValue = this.fees.world.value.toLocaleString();
            const feesCurrency = this.fees.world.currency;

            return `${feesCurrency} ${feesValue} `;
        }
        return 'N/A';
    }

    get budgetString() {
        if (this.budget) {
            const budgetValue = this.budget.value.toLocaleString();
            const budgetCurrency = this.budget.currency;

            return `${budgetCurrency} ${budgetValue}`;
        } else {
            return 'N/A';
        }
    }

    pluralizeSeasons(count) {
        let word = 'сезон';
        if (count % 10 === 1 && count % 100 !== 11) {
            word = 'сезон';
        } else if ([2, 3, 4].includes(count % 10) && ![12, 13, 14].includes(count % 100)) {
            word = 'сезона';
        } else {
            word = 'сезонов';
        }
        return `${count} ${word}`;
    }

    get durationFormatted() {
        if (!this.isSeries && this.movieLength !== null) {
            const hours = Math.floor(this.movieLength / 60);
            const minutes = this.movieLength % 60;

            if (hours === 0) {
                return `${minutes} мин.`;
            } else if (minutes === 0) {
                return `${hours} ч.`;
            } else {
                return `${hours} ч. ${minutes} мин.`;
            }
        }
        if (this.seasons_count && this.seasons_count !== 0) {
            return this.pluralizeSeasons(this.seasons_count);

        }
        return ``;
    }

}
