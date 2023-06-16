import { makeAutoObservable } from "mobx";

class FilmInfoStore {
    constructor({
        title = "",
        year = 0,
        alternativeTitle = "",
        poster_url = "",
        link = "",
        match = 0,
        imdb_rating = 0,
        kinopoisk_rating = 0,
        metacritic = 0,
        duration = 0,
        age = "",
        genres = [""],
        audio_langs = [""],
        subtitles_langs = [""],
        short_description = "",
        countSeasons = 0
    } = {}) {
        this.data = {
            title,
            year,
            alternativeTitle,
            poster_url,
            link,
            match,
            imdb_rating,
            kinopoisk_rating,
            metacritic,
            duration,
            age,
            genres,
            audio_langs,
            subtitles_langs,
            short_description,
            countSeasons
        };

        makeAutoObservable(this);
    }

    setPosterUrl(posterUrl) {
        this.data.poster_url = posterUrl;
    }

    get poster_url() {
        return this.data.poster_url;
    }

    setTitle(title) {
        this.data.title = title;
    }

    get title() {
        return this.data.title;
    }

    setYear(year) {
        this.data.year = year;
    }

    get year() {
        return this.data.year;
    }

    setAlternativeTitle(alternativeTitle) {
        this.data.alternativeTitle = alternativeTitle;
    }

    get alternativeTitle() {
        return this.data.alternativeTitle;
    }

    setMatch(match) {
        this.data.match = match;
    }

    get match() {
        return this.data.match;
    }

    setImdbRating(imdb_rating) {
        this.data.imdb_rating = imdb_rating;
    }

    get imdb_rating() {
        return this.data.imdb_rating;
    }

    setKinopoiskRating(kinopoisk_rating) {
        this.data.kinopoisk_rating = kinopoisk_rating;
    }

    get kinopoisk_rating() {
        return this.data.kinopoisk_rating;
    }

    setMetacritic(metacritic) {
        this.data.metacritic = metacritic;
    }

    get metacritic() {
        return this.data.metacritic;
    }

    setDuration(duration) {
        this.data.duration = duration;
    }

    setAge(age) {
        this.data.age = age;
    }

    get age() {
        return this.data.age;
    }

    setGenres(genres) {
        this.data.genres = genres;
    }

    get genres() {
        return this.data.genres;
    }

    setAudioLangs(audio_langs) {
        this.data.audio_langs = audio_langs;
    }

    get audio_langs() {
        return this.data.audio_langs;
    }

    setSubtitlesLangs(subtitles_langs) {
        this.data.subtitles_langs = subtitles_langs;
    }

    get subtitles_langs() {
        return this.data.subtitles_langs;
    }

    setShortDescription(short_description) {
        this.data.short_description = short_description;
    }

    get short_description() {
        return this.data.short_description;
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
        if (this.data.duration !== 0) {
            const hours = Math.floor(this.data.duration / 60);
            const minutes = this.data.duration % 60;
            if (hours === 0) {
                return `${minutes} мин.`;
            } else if (minutes === 0) {
                return `${hours} ч.`;
            } else {
                return `${hours} ч. ${minutes} мин.`;
            }
        } else if (this.data.countSeries !== 0) {
            return this.pluralizeSeasons(this.data.countSeasons);
        } else {
            return ``;
        }
    }

}


const filmInfoStore = new FilmInfoStore({
    title: 'Бойцовский клуб',
    year: 1999,
    alternativeTitle: 'Fight Club',
    poster_url: 'https://avatars.mds.yandex.net/get-kinopoisk-image/1898899/8ef070c9-2570-4540-9b83-d7ce759c0781/300x450',
    link: 'https://www.kinopoisk.ru/film/361/',
    match: 100,
    imdb_rating: 8.8,
    kinopoisk_rating: 8.7,
    metacritic: 66,
    duration: 154,
    age: 18,
    genres: ['триллер', 'драма', 'криминал'],
    audio_langs: ['ru', 'eng'],
    subtitles_langs: ['ru', 'eng'],
    short_description: 'Страховой работник разрушает рутину своей благополучной жизни. Культовая драма по книге Чака Паланика.'
});

export default filmInfoStore;
