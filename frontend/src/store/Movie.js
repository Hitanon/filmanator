export class Movie {
    constructor(json) {
        this.id = json.id;
        this.fees = json.fees;
        this.rating = json.rating;
        this._match_percentage = json.match_percentage;
        this.movieDuration = json.movieLength;
        this.name = json.name;
        this.description = json.description;
        this.year = json.year;
        this.budget = json.budget;
        this.poster = json.poster;
        this.genres = json.genres;
        this.countries = json.countries;
        this.seasonsInfo = json.seasonsInfo;
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

    get matchPercentage (){
        return `${this._match_percentage}%`;
    }

    set matchPercentage(value) {
        this._match_percentage = value;
    }

    get genresList() {
        return this.genres.map(genre => genre.name).join(', ');
    }

    get countriesList() {
        return this.countries.map(country => country.name).join(', ');
    }

    get actorsList() {
        return this.actors.join(', ');
    }

    get directorsList() {
        return this.directors.join(', ');
    }

    get imdbRating() {
        return this.rating.imdb.toFixed(1);
    }

    get kinopoiskRating() {
        return this.rating.kp.toFixed(1);
    }

    get posterUrl() {
        return this.poster.previewUrl;
    }

    get ageRatingString() {
        return `${this.ageRating}+`;
    }

    get trailerUrl() {
        return this.trailer.url;
    }

    get feesString() {
        const feesValue = this.fees.world.value.toLocaleString();
        const feesCurrency = this.fees.world.currency;

        return `${feesValue} ${feesCurrency}`;
    }

    get budgetString() {
        if (this.budget) {
            const budgetValue = this.budget.value.toLocaleString();
            const budgetCurrency = this.budget.currency;

            return `${budgetValue} ${budgetCurrency}`;
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
        if (!this.isSeries && this.movieDuration !== null) {
            const hours = Math.floor(this.movieDuration / 60);
            const minutes = this.movieDuration % 60;

            if (hours === 0) {
                return `${minutes} мин.`;
            } else if (minutes === 0) {
                return `${hours} ч.`;
            } else {
                return `${hours} ч. ${minutes} мин.`;
            }
        }
        if (this.seasonsInfo && this.seasonsInfo.countSeasons !== 0) {
            return this.pluralizeSeasons(this.seasonsInfo.countSeasons);

        }
        return ``;
    }

}
