import React from "react";

import './style.css';

const SquareButton = ({onClick, icon, size, alt_text }) => {

    const style = {
        width: size,
        height: size,
    };

    return (
        <button onClick={onClick} className="square-button" style={style}>
            <img src={icon} alt={alt_text}/>
        </button>
    );
}

export default SquareButton;