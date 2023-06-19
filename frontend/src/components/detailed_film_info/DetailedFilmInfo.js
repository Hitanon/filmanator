import React, { useState } from "react";
import { observer } from 'mobx-react-lite';
import { filmInfoStore } from '../../store/FilmInfoStore';


import './style.css';
import InfoIcon from "../info_icon/InfoIcon";
import Poster from "../poster_big/Poster";
import SquareButton from "../square_button/SquareButton";

const ICON_HEIGHT = "45px";
const SMALL_ICON_HEIGHT = "35px";
const SQUARE_BUTTON_SIZE = "50px";
const BIG_SQUARE_BUTTON_SIZE = "80px";

const handleBackwardsClick = () => {
    // filmInfoStore.decreaseCurrentMovieIndex();
};

const handleBackwardsEnter = (setIconSrc) => {
    setIconSrc('/img/backwards_button_active.svg');
};

const handleBackwardsLeave = (setIconSrc) => {
    setIconSrc('/img/backwards_button.svg');
};


const DetailedFilmInfo = observer(() => {
    const [backwardsSrc, setBackwardsSrc] = useState('/img/backwards_button.svg');

    return (
        <div className="container-grid">
            <button onClick={handleBackwardsClick} className="backwards-button"
                onMouseEnter={() => handleBackwardsEnter(setBackwardsSrc)}
                onMouseLeave={() => handleBackwardsLeave(setBackwardsSrc)}
            >
                <img src={backwardsSrc} alt="Backward" />
            </button>
            <div className="poster">
                <Poster className='poster' imageUrl={filmInfoStore.currentMovie.posterUrl} />
            </div>

            <div className="big_rate_buttons-container">
                <SquareButton icon="/img/like_icon.svg" size={BIG_SQUARE_BUTTON_SIZE} alt_text="like" />
                <SquareButton icon="/img/dislike_icon.svg" size={BIG_SQUARE_BUTTON_SIZE} alt_text="dislike" />
                <SquareButton icon="/img/share_icon.svg" size={BIG_SQUARE_BUTTON_SIZE} alt_text="share" />
            </div>

            <h1 className="h1">{filmInfoStore.currentMovie.title}</h1>
            <h2 className="h2">{filmInfoStore.currentMovie.alternativeTitle}</h2>


            <div className="icons-row">
                <InfoIcon icon="/img/time_icon.svg" text={filmInfoStore.currentMovie.durationFormatted} color='#FFFFFF' height={SMALL_ICON_HEIGHT} />
                <InfoIcon text={filmInfoStore.currentMovie.ageRatingString} color='#FFFFFF' height={SMALL_ICON_HEIGHT} />
            </div>

            <h3 className="h3">{filmInfoStore.currentMovie.shortDescription}</h3>

            <div className="rating_icons">
                <InfoIcon icon="/img/match_icon.svg" text={`${filmInfoStore.currentMovie.matchPercentage}`} color='#F66004' height={ICON_HEIGHT} />
                <InfoIcon icon="/img/imdb_icon.svg" text={`${filmInfoStore.currentMovie.imdbRating}`} color='#FFFFFF' height={ICON_HEIGHT} />
                <InfoIcon icon="/img/kinopoisk_icon.svg" text={`${filmInfoStore.currentMovie.kinopoiskRating}`} color='#FFFFFF' height={ICON_HEIGHT} />
            </div>

            <div className="trailer-button-container">
                <p className="p">Трейлер: </p>
                <SquareButton icon="/img/youtube_icon.svg" size={SQUARE_BUTTON_SIZE} alt_text="trailer" />
            </div>

            <div className="watch-button-container">
                <p className="p">Смотреть полностью: </p>
                <SquareButton icon="/img/kinopoisk_icon.svg" size={SQUARE_BUTTON_SIZE} alt_text="link" />
            </div>

            <div className="about">
                О фильме
            </div>

            <div className="info" style={{ gridRow: "7" }}>
                Жанр: {filmInfoStore.currentMovie.genresList}
            </div>

            <div className="info" style={{ gridRow: "8" }}>
                Страна: {filmInfoStore.currentMovie.countriesList}
            </div>

            <div className="info" style={{ gridRow: "9" }}>
                Год: {filmInfoStore.currentMovie.year}
            </div>

            <div className="info" style={{ gridRow: "10" }}>
                Режиссер: {filmInfoStore.currentMovie.directorsList}
            </div>

            <div className="info" style={{ gridRow: "11" }}>
                Бюджет: {filmInfoStore.currentMovie.budgetString}
            </div>

            <div className="info" style={{ gridRow: "12" }}>
                Сборы: {filmInfoStore.currentMovie.feesString}
            </div>

            <div className="about" style={{ gridRow: "13" }}>
                Сюжет
            </div>

            <div className="plot" style={{ gridRow: "14" }}>
                {filmInfoStore.currentMovie.description}
            </div>

            <div className="similar" style={{ gridRow: "15" }}>
                Похожие фильмы
            </div>

            <div className="actors-container">
                <h3 className="actors-title">
                    Главные роли:
                </h3>
                <p className="actors">
                    {filmInfoStore.currentMovie.actorsList}
                </p>
            </div>

        </div>
    );
});

export default DetailedFilmInfo;