import React from "react";

import './style.css';

const SquareButtonBig = ({onClick, icon, size, alt_text }) => {

    const style = {
        width: size,
        height: size,
    };

    return (
        <button onClick={onClick} className="square-button-big" style={style}>
            <img src={icon} alt={alt_text}/>
        </button>
    );
}

export default SquareButtonBig;