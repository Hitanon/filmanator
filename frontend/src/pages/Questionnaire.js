import React, { useState, useEffect } from "react";
import Footer from "../components/footer/Footer";
import Navbar from "../components/navbar/Navbar";
import Question from "../components/question/Question";


const Questionnaire = () => {
    const [showQuesiton, setShowQuestion] = useState(false);

    const checkLoadImage = () => {
        const image = new Image();
        image.src = "/img/filmanator_questionnaire.webp";
        image.onload = () => setShowQuestion(true);
    }

    useEffect(() => {
        checkLoadImage();
    }, []);

    return (
        <div className="questionnaire-page">
            <Navbar />
            <div className="image-container">
                <img className="filmanator-questionnaire-image"
                    src="/img/filmanator_questionnaire.webp"
                    alt="Filmanator for questionnaire"
                />
               {showQuesiton && <Question />} 
            </div>
            <Footer />
        </div>
    );
}

export default Questionnaire;