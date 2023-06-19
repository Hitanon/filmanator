import React from 'react';
import './style.css';

const Poster = ({ imageUrl }) => {
    return (
        <div className="poster-container">
            <img src={imageUrl} alt="Poster" />
        </div>
    );
};

export default Poster;