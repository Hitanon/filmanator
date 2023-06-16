import React, { useState, useEffect, useCallback } from 'react';
import { observer } from 'mobx-react-lite';
import './style.css'
import AnimatedText from '../animated_text/AnimatedText';
import questionStore from '../../store/QuestionStore';

const handleMouseEnter = (setIconSrc) => {
    setIconSrc('/img/previous_question_button_active.svg');
};

const handleMouseLeave = (setIconSrc) => {
    setIconSrc('/img/previous_question_button.svg');
};

const handleButtonClick = async (answer) => {
    console.log(answer)
    questionStore.setQuestionNumber(2);
    questionStore.setQuestionText("Тест обновления вопроса");
    questionStore.setAnswers(['ответ 1', 'ответ 2', 'ответ 3']);
};

const updateCurrentButtonIndex = (isTextAnimated, currentButtonIndex, setCurrentButtonIndex) => {
    if (isTextAnimated && currentButtonIndex < questionStore.answers.length - 1) {
        const timeout = setTimeout(() => {
            setCurrentButtonIndex(currentButtonIndex + 1);
        }, 100);
        return () => clearTimeout(timeout);
    }
};

const Question = observer(() => {
    const [iconSrc, setIconSrc] = useState('/img/previous_question_button.svg');
    const [currentButtonIndex, setCurrentButtonIndex] = useState(-1);
    const [isTextAnimated, setIsTextAnimated] = useState(false);

    const handleAnimationComplete = useCallback(() => {
        setIsTextAnimated(true);
    }, []);

    useEffect(() => {
        updateCurrentButtonIndex(isTextAnimated, currentButtonIndex, setCurrentButtonIndex);
    }, [isTextAnimated, currentButtonIndex]);

    return (
        <div className="question-container">
            <div className="question-header">
                <button className="back-button"
                    onMouseEnter={() => handleMouseEnter(setIconSrc)}
                    onMouseLeave={() => handleMouseLeave(setIconSrc)}
                >
                    <img src={iconSrc} alt="Back" />
                </button>
                <div className="question-number">Вопрос {questionStore.questionNumber}</div>
            </div>
            <div className="question-text">
                <AnimatedText
                    text={questionStore.questionText}
                    onComplete={handleAnimationComplete}
                />
            </div>
            <div className="button-container">
                {questionStore.answers.map((text, index) => (
                    index <= currentButtonIndex && (
                        <button key={index} className="answer-button" onClick={() => handleButtonClick(text)}>
                            {text}
                        </button>
                    )
                ))}
            </div>
        </div>
    );
});

export default Question;
