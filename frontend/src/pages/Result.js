import React, {useState, useEffect} from "react";
import Footer from "../components/footer/Footer";
import Navbar from "../components/navbar/Navbar";
import FilmInfo from "../components/film_info/FilmInfo";



const Result = () => {
    const [showFilmInfo, setShowFilmInfo] = useState(false);

    const checkLoadImage = () => {
        const image = new Image();
        image.src = "/img/filmanator_result.webp";
        image.onload = () => setShowFilmInfo(true);
    }

    useEffect(() => {
        checkLoadImage();
    }, []);

    return (
        <div className="questionnaire-page">
            <Navbar />
            <div className="image-container">
                <img className="filmanator-result-image"
                    src="/img/filmanator_result.webp"
                    alt="Filmanator for questionnaire"
                />
                {showFilmInfo && <FilmInfo />}
            </div>
            <Footer />
        </div>
    );
}

export default Result;