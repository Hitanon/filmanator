import { makeAutoObservable } from "mobx";

class FilmInfoStore {
    constructor(title,
        year,
        alternativeTitle,
        poster_url,
        link,
        match,
        imdb_rating,
        kinopoisk_rating,
        metacritic,
        length,
        age,
        genres,
        audio_langs,
        subtitles_langs,
        short_description) {
        if (arguments.length === 0) {
            this.title = '';
            this.year = 0;
            this.alternativeTitle = '';
            this.poster_url = '';
            this.link = '';
            this.match = 0;
            this.imdb_rating = 0;
            this.kinopoisk_rating = 0;
            this.metacritic = 0;
            this.length = 0;
            this.age = '';
            this.genres = [''];
            this.audio_langs = [''];
            this.subtitles_langs = [''];
            this.short_description = 0;
        } else {
            this.title = title;
            this.year = year;
            this.alternativeTitle = alternativeTitle;
            this.poster_url = poster_url;
            this.link = link;
            this.match = match;
            this.imdb_rating = imdb_rating;
            this.kinopoisk_rating = kinopoisk_rating;
            this.metacritic = metacritic;
            this.length = length;
            this.age = age;
            this.genres = genres;
            this.audio_langs = audio_langs;
            this.subtitles_langs = subtitles_langs;
            this.short_description = short_description;
        }

        makeAutoObservable(this);
    }

    setPosterUrl(posterUrl) {
        this.poster_url = posterUrl;
    }

    setTitle(title) {
        this.title = title;
    }

    setYear(year) {
        this.year = year;
    }

    setAlternativeTitle(alternativeTitle) {
        this.alternativeTitle = alternativeTitle;
    }

    setMatch(match) {
        this.match = match;
    }

    setImdbRating(imdb_rating) {
        this.imdb_rating = imdb_rating;
    }

    setKinopoiskRating(kinopoisk_rating) {
        this.kinopoisk_rating = kinopoisk_rating;
    }

    setMetacritic(metacritic) {
        this.metacritic = metacritic;
    }

    setLength(length) {
        this.length = length;
    }

    setAge(age) {
        this.age = age;
    }

    setGenres(genres) {
        this.genres = genres;
    }

    setAudioLangs(audio_langs) {
        this.audio_langs = audio_langs;
    }

    setSubtitlesLangs(subtitles_langs) {
        this.subtitles_langs = subtitles_langs;
    }

    setShortDescription(short_description) {
        this.short_description = short_description;
    }

    get lengthFormatted() {
        const hours = Math.floor(this.length / 60);
        const minutes = this.length % 60;

        if (hours === 0) {
            return `${minutes} мин.`;
        } else if (minutes === 0) {
            return `${hours} ч.`;
        } else {
            return `${hours} ч. ${minutes} мин.`;
        }
    }
}

const filmInfoStore = new FilmInfoStore(
    'Бойцовский клуб',
    1999,
    'Fight Club',
    'https://avatars.mds.yandex.net/get-kinopoisk-image/1898899/8ef070c9-2570-4540-9b83-d7ce759c0781/300x450',
    'https://www.kinopoisk.ru/film/361/',
    100,
    8.8,
    8.7,
    66,
    154,
    18,
    ['триллер', 'драма', 'криминал'],
    ['ru', 'eng'],
    ['ru', 'eng'],
    'Страховой работник разрушает рутину своей благополучной жизни. Культовая драма по книге Чака Паланика.'
);
export default filmInfoStore;
