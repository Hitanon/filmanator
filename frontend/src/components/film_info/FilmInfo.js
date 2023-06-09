import React, { useState, useEffect } from "react";
import { observer } from 'mobx-react-lite';
import { useNavigate } from "react-router-dom";

import { filmInfoStore } from '../../store/FilmInfoStore';

import './style.css';
import { QUESTIONNAIRE_ROUTE, DETAILED_RESULT_ROUTE } from "../../utils/Consts";
import InfoIcon from "../info_icon/InfoIcon";
import Poster from "../poster/Poster";
import SquareButton from "../square_button/SquareButton";
import SharePopup from "../share_popup/SharePopup";


// rate buttons size
const SQUARE_BUTTON_SIZE = "2.7vw";
const ICON_HEIGHT = "2vw";
const NAV_BUTTON_WIDTH = "5vw";


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


const handleWatchClick = () => {
    filmInfoStore.redirectKinopoisk();
};

const handleBackwardsClick = () => {
    filmInfoStore.decreaseCurrentMovieIndex();
};


const handleForwardsClick = () => {
    filmInfoStore.increaseCurrentMovieIndex();
};


const FilmInfo = observer(() => {

    // navigator
    const navigate = useNavigate();

    const handleLearnMoreClick = () => {
        navigate(DETAILED_RESULT_ROUTE);
    };

    const handleRepeatClick = () => {
        navigate(QUESTIONNAIRE_ROUTE);
    };

    const handleShareClick = () => {
        setIsSharePopupOpen(true);
    };

    const handleSharePopupClose = () => {
        setIsSharePopupOpen(false);
    };

    const [isSharePopupOpen, setIsSharePopupOpen] = useState(false);
    const [backwardsSrc, setBackwardsSrc] = useState('/img/backwards_button.svg');
    const [forwardsSrc, setForwardsSrc] = useState('/img/forwards_button.svg');
    const { currentMovieIndex, movies } = filmInfoStore;


    useEffect(() => {
        if (currentMovieIndex === movies.length - 1) {
            setForwardsSrc('/img/forwards_button.svg');
        }
    }, [currentMovieIndex, movies.length, setForwardsSrc]);

    useEffect(() => {
        if (currentMovieIndex === 0) {
            setBackwardsSrc('/img/backwards_button.svg');
        }
    }, [currentMovieIndex, setBackwardsSrc]);


    return (
        <>
            {isSharePopupOpen && (
                <>
                    <div className="overlay" onClick={handleSharePopupClose} />
                    <SharePopup
                        title={filmInfoStore.currentMovie.title}
                        link={filmInfoStore.currentMovie.link}
                        isSeries={filmInfoStore.currentMovie.isSeries}
                        onClose={handleSharePopupClose}
                    />
                </>
            )}
            <div className="film-info-container">

                <Poster width='8vw' imageUrl={filmInfoStore.currentMovie.posterUrl} />

                <h1>{filmInfoStore.currentMovie.title}</h1>
                <h2>{filmInfoStore.currentMovie.alternativeTitle}</h2>

                <div className="icon-container">
                    <div className="icon-row">
                        <InfoIcon icon="/img/match_icon.svg" text={`${filmInfoStore.currentMovie.matchPercentage}`} color='#F66004' height={ICON_HEIGHT} />
                        <InfoIcon icon="/img/imdb_icon.svg" text={`${filmInfoStore.currentMovie.imdbRating}`} color='#FFFFFF' height={ICON_HEIGHT} />
                        <InfoIcon icon="/img/kinopoisk_icon.svg" text={`${filmInfoStore.currentMovie.kinopoiskRating}`} color='#FFFFFF' height={ICON_HEIGHT} />
                    </div>
                    <div className="icon-row">
                        <InfoIcon icon="/img/time_icon.svg" text={filmInfoStore.currentMovie.durationFormatted} color='#FFFFFF' height={ICON_HEIGHT} />
                        <InfoIcon text={filmInfoStore.currentMovie.ageRatingString} color='#FFFFFF' height={ICON_HEIGHT} />
                    </div>
                </div>

                <div className="info-container">
                    <p>Жанр: {filmInfoStore.currentMovie.genresList}</p>
                    <p>Страна: {`${filmInfoStore.currentMovie.countriesList}`}</p>
                    <p>Режиссер: {filmInfoStore.currentMovie.directorsList}</p>
                </div>

                <div className="description-container">
                    <h3>Краткое описание: </h3>
                    <p>{filmInfoStore.currentMovie.shortDescription}</p>
                </div>

                <div className="rate_buttons-container">
                    <SquareButton onClick={handleWatchClick} icon="/img/kinopoisk_icon.svg" size={SQUARE_BUTTON_SIZE} alt_text="link" />
                    <SquareButton onClick={handleShareClick} icon="/img/share_icon.svg" size={SQUARE_BUTTON_SIZE} alt_text="share" />
                </div>


                <div className="actions_container">
                    {filmInfoStore.currentMovieIndex > 0 ? (
                        <button onClick={handleBackwardsClick} className="nav-button"
                            onMouseEnter={() => handleBackwardsEnter(setBackwardsSrc)}
                            onMouseLeave={() => handleBackwardsLeave(setBackwardsSrc)}
                        >
                            <img src={backwardsSrc} alt="Backward" />
                        </button>
                    ) : (
                        <div style={{ minWidth: NAV_BUTTON_WIDTH }}></div>
                    )}

                    <button onClick={handleRepeatClick} className="repeat-button">
                        Пройти опрос заново
                    </button>

                    <button onClick={handleLearnMoreClick} className="learn-more-button">
                        Подробнее
                    </button>

                    {filmInfoStore.currentMovieIndex < filmInfoStore.movies.length - 1 ? (
                        <button onClick={handleForwardsClick} className="nav-button"
                            onMouseEnter={() => handleForwardsEnter(setForwardsSrc)}
                            onMouseLeave={() => handleForwardsLeave(setForwardsSrc)}
                        >
                            <img src={forwardsSrc} alt="Forward" />
                        </button>
                    ) : (
                        <div style={{ width: NAV_BUTTON_WIDTH }}></div>
                    )}
                </div>
            </div>
        </>
    );
});

export default FilmInfo;