import React from "react";
// import { observer } from 'mobx-react-lite';
// import filmInfoStore from '../../store/FilmInfoStore';


import './style.css';
// import InfoIcon from "../info_icon/InfoIcon";
// import Poster from "../poster/Poster";
// import SquareButton from "../square_button/SquareButton";

// const ICON_HEIGHT = "3vw";

const DetailedFilmInfo = () => {
    return (
        <div className="container-grid">
            {/* <div className="poster">
                <Poster className='poster' width='auto' height='auto' imageUrl={filmInfoStore.poster_url} />
            </div> */}
            {/* <h1 className="header">{filmInfoStore.title} ({filmInfoStore.year})</h1> */}
            <div className="rating_icons">
            </div>
        </div>
    );
}

export default DetailedFilmInfo;