import React, { useEffect } from "react";
import Footer from "../components/footer/Footer";
import Navbar from "../components/navbar/Navbar";
import Question from "../components/question/Question";

const Questionnaire = () => {

    useEffect(() => {
        document.body.classList.add('questionnairepage');
        return () => {
            document.body.classList.remove('questionnairepage');
        }
    }, []);

    const handleBackClick = () => {
        // Handle back button click here
        console.log('Back button clicked');
    };

    return (
        <>
            <Navbar />
            <div className="image-container">
                <img className="filmanator-questionnaire-image"
                    src="/img/filmanator_questionnaire.png"
                    alt="Filmanator for questionnaire"
                />
                <Question
                    questionNumber={1}
                    questionText="Фильмы какого жанра тебе нравятся больше?"
                    buttonTexts={['Комедии', 'Документальные', 'Ужасы', 'Исторические', 'Другое']}
                    onBackClick={handleBackClick}
                />
            </div>
            <Footer />
        </>
    );
}

export default Questionnaire;