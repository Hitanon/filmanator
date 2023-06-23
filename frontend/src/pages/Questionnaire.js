import React from "react";
import Footer from "../components/footer/Footer";
import Navbar from "../components/navbar/Navbar";
import Question from "../components/question/Question";


const Questionnaire = () => {

    return (
        <div className="questionnaire-page">
            <Navbar />
            <div className="image-container">
                <img className="filmanator-questionnaire-image"
                    src="/img/filmanator_questionnaire.webp"
                    alt="Filmanator for questionnaire"
                />
                <Question />
            </div>
            <Footer />
        </div>
    );
}

export default Questionnaire;