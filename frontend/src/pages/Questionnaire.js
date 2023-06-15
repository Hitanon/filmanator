import React, { useEffect } from "react";
import {addBodyClass, removeBodyClass} from "../utils/BodyClassLoader";
import Footer from "../components/footer/Footer";
import Navbar from "../components/navbar/Navbar";
import Question from "../components/question/Question";


const Questionnaire = () => {

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
                <img className="filmanator-questionnaire-image"
                    src="/img/filmanator_questionnaire.png"
                    alt="Filmanator for questionnaire"
                />
                <Question/>
            </div>
            <Footer />
        </>
    );
}

export default Questionnaire;