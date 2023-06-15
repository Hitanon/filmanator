import React, { useEffect } from "react";
import { addBodyClass, removeBodyClass } from "../utils/BodyClassLoader";
import Footer from "../components/footer/Footer";
import Navbar from "../components/navbar/Navbar";
import FilmInfo from "../components/film_info/FilmInfo";



const Result = () => {

    useEffect(() => {
        addBodyClass('questionnaire-bg');
        return () => {
            removeBodyClass('questionnaire-bg');
        }
    }, []);

    return (
        <>
            <Navbar />
            <div className="image-container">
                <img className="filmanator-result-image"
                    src="/img/filmanator_result.png"
                    alt="Filmanator for questionnaire"
                />
                <FilmInfo />
            </div>
            <Footer />
        </>
    );
}

export default Result;