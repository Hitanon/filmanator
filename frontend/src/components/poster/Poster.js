import React from 'react';
import './style.css';

const Poster = ({ width, imageUrl }) => {
    return (
        <div className="poster-container" style={{ width}}>
            <img src={imageUrl} alt="Poster" />
        </div>
    );
};

export default Poster;