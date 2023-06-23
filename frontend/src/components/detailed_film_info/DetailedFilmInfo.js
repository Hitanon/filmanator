import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { observer } from 'mobx-react-lite';
import { filmInfoStore } from '../../store/FilmInfoStore';


import './style.css';
import InfoIconBig from "../info_icon_big/InfoIconBig";
import BigPoster from "../poster_big/BigPoster";
import SquareButtonBig from "../square_button_big/SquareButtonBig";

const ICON_HEIGHT = "45px";
const SMALL_ICON_HEIGHT = "35px";
const SQUARE_BUTTON_SIZE = "50px";
const BIG_SQUARE_BUTTON_SIZE = "80px";
const ICON_FONT_SIZE = "18px";
const SMALL_ICON_FONT_SIZE = "16px";


const handleBackwardsEnter = (setIconSrc) => {
    setIconSrc('/img/backwards_button_active.svg');
};

const handleBackwardsLeave = (setIconSrc) => {
    setIconSrc('/img/backwards_button.svg');
};

const handleWatchClick = () => {
    filmInfoStore.redirectKinopoisk();
};

const handleTrailerClick = () => {
    filmInfoStore.redirectYouTube();
};

const DetailedFilmInfo = observer(() => {
    const navigate = useNavigate();

    const handleBackwardsClick = () => {
        navigate(-1);
    };


    const [backwardsSrc, setBackwardsSrc] = useState('/img/backwards_button.svg');

    return (
        <div className="container">
            <div className="container-grid-1">
                <button onClick={handleBackwardsClick} className="backwards-button"
                    onMouseEnter={() => handleBackwardsEnter(setBackwardsSrc)}
                    onMouseLeave={() => handleBackwardsLeave(setBackwardsSrc)}
                >
                    <img src={backwardsSrc} alt="Backward" />
                </button>
                <div className="poster">
                    <BigPoster imageUrl={filmInfoStore.currentMovie.posterUrl} />
                </div>
                <div className="rate-buttons-big-container">
                    <SquareButtonBig icon="/img/like_icon.svg" size={BIG_SQUARE_BUTTON_SIZE} alt_text="like" />
                    <SquareButtonBig icon="/img/dislike_icon.svg" size={BIG_SQUARE_BUTTON_SIZE} alt_text="dislike" />
                    <SquareButtonBig icon="/img/share_icon.svg" size={BIG_SQUARE_BUTTON_SIZE} alt_text="share" />
                </div>
            </div>


            <div className="container-grid-2">
                <h1 className="h1">{filmInfoStore.currentMovie.title}</h1>
                <h2 className="h2">{filmInfoStore.currentMovie.alternativeTitle}</h2>
                <div className="icons-row">
                    <InfoIconBig
                        icon="/img/time_icon.svg"
                        text={filmInfoStore.currentMovie.durationFormatted}
                        color='#FFFFFF' height={SMALL_ICON_HEIGHT}
                        fontSize={SMALL_ICON_FONT_SIZE} />
                    <InfoIconBig text={filmInfoStore.currentMovie.ageRatingString}
                        color='#FFFFFF'
                        height={SMALL_ICON_HEIGHT}
                        fontSize={SMALL_ICON_FONT_SIZE} />
                </div>
                <h3 className="h3">{filmInfoStore.currentMovie.shortDescription}</h3>

                <div className="trailer-button-container">
                    <p className="p">Трейлер: </p>
                    <SquareButtonBig icon="/img/youtube_icon.svg" size={SQUARE_BUTTON_SIZE} onClick={handleTrailerClick} alt_text="trailer" />
                </div>

                <div className="watch-button-container">
                    <p className="p">Смотреть полностью: </p>
                    <SquareButtonBig icon="/img/kinopoisk_icon.svg" size={SQUARE_BUTTON_SIZE} onClick={handleWatchClick} alt_text="link" />
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
            </div>


            <div className="container-grid-3">
                <div className="rating_icons">
                    <InfoIconBig icon="/img/match_icon.svg"
                        text={`${filmInfoStore.currentMovie.matchPercentage}`}
                        color='#F66004'
                        height={ICON_HEIGHT}
                        fontSize={ICON_FONT_SIZE} />
                    <InfoIconBig icon="/img/imdb_icon.svg"
                        text={`${filmInfoStore.currentMovie.imdbRating}`}
                        color='#FFFFFF'
                        height={ICON_HEIGHT}
                        fontSize={ICON_FONT_SIZE} />
                    <InfoIconBig icon="/img/kinopoisk_icon.svg"
                        text={`${filmInfoStore.currentMovie.kinopoiskRating}`}
                        color='#FFFFFF'
                        height={ICON_HEIGHT}
                        fontSize={ICON_FONT_SIZE} />
                </div>
                <div className="actors-container">
                    <h3 className="actors-title">
                        Главные роли:
                    </h3>
                    <div className="actors">
                        {filmInfoStore.currentMovie.actorsList}
                    </div>
                </div>
            </div>
        </div>
    );
});

export default DetailedFilmInfo;