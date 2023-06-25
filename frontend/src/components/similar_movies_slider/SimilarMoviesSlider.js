import React, { useState, useEffect } from "react";

import './style.css';
import SimilarMovie from "../similar_movie/SimilarMovie";

// Left button
const handleLeftEnter = (setIconSrc) => {
    setIconSrc('/img/backwards_button_active.svg');
};

const handleLeftLeave = (setIconSrc) => {
    setIconSrc('/img/backwards_button.svg');
};

// Right button
const handleRightEnter = (setIconSrc) => {
    setIconSrc('/img/forwards_button_active.svg');
};

const handleRightLeave = (setIconSrc) => {
    setIconSrc('/img/forwards_button.svg');
};


const SimilarMoviesSlider = ({ movies }) => {
    const [startIndex, setStartIndex] = useState(0);
    const [leftSrc, setLeftSrc] = useState('/img/backwards_button.svg');
    const [rightSrc, setRightSrc] = useState('/img/forwards_button.svg');

    useEffect(() => {
        setLeftSrc('/img/backwards_button.svg');
        setRightSrc('/img/forwards_button.svg');
    }, [startIndex]);
    

    function handleLeftClick() {
        setStartIndex(startIndex => Math.max(0, startIndex - 3));
    }

    function handleRightClick() {
        setStartIndex(startIndex => Math.min(movies.length - 3, startIndex + 3));
    }

    return (
        <>
            {movies && movies.length > 0 ? (
                <div className="MovieSlider">
                    {startIndex !== 0 ? (
                        <button className="MovieSlider-icon" onClick={handleLeftClick}
                            onMouseEnter={() => handleLeftEnter(setLeftSrc)}
                            onMouseLeave={() => handleLeftLeave(setLeftSrc)}>
                            <img className="Icon-button" src={leftSrc} alt="Left" />
                        </button>
                    ) : (
                        <div className="MovieSlider-placeholder"></div>
                    )}
                    {movies.slice(startIndex, startIndex + 4).map(movie => (
                        <SimilarMovie key={movie.id} movie={movie} />
                    ))}
                    {startIndex + 4 < movies.length ? (
                        <button className="MovieSlider-icon" onClick={handleRightClick}
                            onMouseEnter={() => handleRightEnter(setRightSrc)}
                            onMouseLeave={() => handleRightLeave(setRightSrc)}>
                            <img className="Icon-button" src={rightSrc} alt="Right" />
                        </button>
                    ) : (
                        <div className="MovieSlider-placeholder"></div>
                    )}
                </div>
            ) : (
                <div className="No-similar">Нет похожих</div>
            )}
        </>
    );
}

export default SimilarMoviesSlider;