import React from 'react';
import './style.css';

const Poster = ({ imageUrl, title, rating, showCircleIcon }) => {
  return (
    <div className="poster-container">
      <div className="poster-image-container">
        <img src={imageUrl} alt={title} className="poster-image" />
      </div>
      <div className="poster-title">{title}</div>
      <div className="poster-rating-container">
        <div className="poster-rating-icon" />
        <div className="poster-rating-text">{rating}</div>
      </div>
      {showCircleIcon && <div className="poster-circle-icon" />}
    </div>
  );
};

export default Poster;
