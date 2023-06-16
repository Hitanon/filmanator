import React from "react";
import Footer from "../components/footer/Footer";
import Navbar from "../components/navbar/Navbar";
import FilmInfo from "../components/film_info/FilmInfo";



const Result = () => {

    return (
        <div className="questionnaire-page">
            <Navbar />
            <div className="image-container">
                <img className="filmanator-result-image"
                    src="/img/filmanator_result.png"
                    alt="Filmanator for questionnaire"
                />
                <FilmInfo />
            </div>
            <Footer />
        </div>
    );
}

export default Result;