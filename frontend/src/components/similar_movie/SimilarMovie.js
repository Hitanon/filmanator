import React from "react";

import './style.css';




const SimilarMovie = ({ movie }) => {

    const handleMovieClick = () => {
        if (movie.link) {
            window.open(movie.link, '_blank');
        }
    }

    return (
        <>
            <div className="Movie" onClick={handleMovieClick}>
                <img className="Movie-poster"src={movie.poster.previewUrl} alt={movie.name} />

                <div className="Movie-rating">
                    <img className="Icon-rating" src="/img/imdb_rating_small_icon.png" alt="IMDB" />
                    {movie.rating.toFixed(1)}
                </div>
                <div className="Movie-name">{movie.name}</div>
            </div>

        </>
    );
}

export default SimilarMovie;
