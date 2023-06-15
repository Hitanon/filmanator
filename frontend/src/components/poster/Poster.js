import React from 'react';
import './style.css';

const Poster = ({ width, height, imageUrl }) => {
    return (
        <div className="poster-container" style={{ width, height }}>
            <img src={imageUrl} alt="Poster" />
        </div>
    );
};

export default Poster;