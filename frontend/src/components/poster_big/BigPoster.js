import React from 'react';
import './style.css';

const BigPoster = ({ imageUrl }) => {
    return (
        <div className="big-poster-container">
            <img src={imageUrl} alt="Poster" />
        </div>
    );
};

export default BigPoster;