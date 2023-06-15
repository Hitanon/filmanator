import React, { useState } from "react";
import { observer } from 'mobx-react-lite';
import filmInfoStore from '../../store/FilmInfoStore';

import './style.css';
import InfoIcon from "../info_icon/InfoIcon";
import Poster from "../poster/Poster";
import SquareButton from "../square_button/SquareButton";

// rate buttons size
const SQUARE_BUTTON_SIZE = "2.7vw";

// backwards button
const handleBackwardsEnter = (setIconSrc) => {
    setIconSrc('/img/backwards_button_active.svg');
};

const handleBackwardsLeave = (setIconSrc) => {
    setIconSrc('/img/backwards_button.svg');
};

const handleForwardsEnter = (setIconSrc) => {
    setIconSrc('/img/forwards_button_active.svg');
};

// forwards button
const handleForwardsLeave = (setIconSrc) => {
    setIconSrc('/img/forwards_button.svg');
};

//Handles
const handleLikeClick = () => {
    console.log("pressed like")
};

const handleDislikeClick = () => {
    console.log("pressed dislike")
};

const handleShareClick = () => {
    console.log("pressed share")
};

const handleWatchClick = () => {
    console.log("pressed watch")
};

const handleBackwardsClick = () => {
    console.log("pressed backwards")
};

const handleLearnMoreClick = () => {
    console.log("pressed learn more")
};

const handleRepeatClick = () => {
    console.log("pressed repeat")
};

const handleForwardsClick = () => {
    console.log("pressed forwards")
};


const FilmInfo = observer(() => {

    const [backwardsSrc, setBackwardsSrc] = useState('/img/backwards_button.svg');
    const [forwardsSrc, setForwardsSrc] = useState('/img/forwards_button.svg');

    return (
        <div className="film-info-container">

            <Poster width='8vw' height='12vw' imageUrl={filmInfoStore.poster_url} />

            <h1>{filmInfoStore.title} ({filmInfoStore.year})</h1>
            <h2>{filmInfoStore.alternativeTitle}</h2>

            <div className="icon-container">
                <div className="icon-row">
                    <InfoIcon icon="/img/match_icon.svg" text={`${filmInfoStore.match}%`} color='#F66004' />
                    <InfoIcon icon="/img/imdb_icon.svg" text={`${filmInfoStore.imdb_rating}`} color='#FFFFFF' />
                    <InfoIcon icon="/img/kinopoisk_icon.svg" text={`${filmInfoStore.kinopoisk_rating}`} color='#FFFFFF' />
                    <InfoIcon icon="/img/metacritic_icon.svg" text={`${filmInfoStore.metacritic}`} color='#FFFFFF' />
                </div>
                <div className="icon-row">
                    <InfoIcon icon="/img/time_icon.svg" text={`${filmInfoStore.lengthFormatted}`} color='#FFFFFF' />
                    <InfoIcon text={`${filmInfoStore.age}+`} color='#FFFFFF' />
                </div>
            </div>

            <div className="info-container">
                <p>Жанры: {filmInfoStore.genres.join(', ')}</p>
                <p>Озвучка: {filmInfoStore.audio_langs.join(', ')}</p>
                <p>Субтитры: {filmInfoStore.subtitles_langs.join(', ')}</p>
            </div>

            <div className="description-container">
                <h3>Краткое описание: </h3>
                <p>{filmInfoStore.short_description}</p>
            </div>

            <div className="rate_buttons-container">
                <SquareButton onClick={handleLikeClick} icon="/img/like_icon.svg" size={SQUARE_BUTTON_SIZE} alt_text="like" />
                <SquareButton onClick={handleDislikeClick} icon="/img/dislike_icon.svg" size={SQUARE_BUTTON_SIZE} alt_text="dilike" />
                <SquareButton onClick={handleShareClick} icon="/img/share_icon.svg" size={SQUARE_BUTTON_SIZE} alt_text="share" />
            </div>

            <div className="watch_buttons-container">
                <p>Смотреть: </p>
                <SquareButton onClick={handleWatchClick} icon="/img/kinopoisk_icon.svg" size={SQUARE_BUTTON_SIZE} alt_text="link" />
            </div>

            <div className="actions_container">
                <button onClick={handleBackwardsClick}  className="nav-button"
                    onMouseEnter={() => handleBackwardsEnter(setBackwardsSrc)}
                    onMouseLeave={() => handleBackwardsLeave(setBackwardsSrc)}
                >
                    <img src={backwardsSrc} alt="Backward" />
                </button>

                <button onClick={handleRepeatClick} className="repeat-button">
                    Пройти опрос заново
                </button>

                <button onClick={handleLearnMoreClick} className="learn-more-button">
                    Подробнее
                </button>

                <button onClick={handleForwardsClick} className="nav-button"
                    onMouseEnter={() => handleForwardsEnter(setForwardsSrc)}
                    onMouseLeave={() => handleForwardsLeave(setForwardsSrc)}
                >
                    <img src={forwardsSrc} alt="Forward" />
                </button>
            </div>


        </div>
    );
});

export default FilmInfo;