import React, { useState, useEffect, useCallback } from 'react';
import './style.css'
import AnimatedText from '../animated_text/AnimatedText';

const Question = ({ questionNumber, questionText, buttonTexts, onBackClick }) => {
    const [iconSrc, setIconSrc] = useState('/img/previous_question_button.svg');
    const [currentButtonIndex, setCurrentButtonIndex] = useState(-1);
    const [isTextAnimated, setIsTextAnimated] = useState(false);

    const handleMouseEnter = () => {
        setIconSrc('/img/previous_question_button_active.svg');
    };

    const handleMouseLeave = () => {
        setIconSrc('/img/previous_question_button.svg');
    };

    const handleAnimationComplete = useCallback(() => {
        setIsTextAnimated(true);
    }, []);

    useEffect(() => {
        if (isTextAnimated && currentButtonIndex < buttonTexts.length - 1) {
            const timeout = setTimeout(() => {
                setCurrentButtonIndex(currentButtonIndex + 1);
            }, 100);
            return () => clearTimeout(timeout);
        }
    }, [isTextAnimated, currentButtonIndex, buttonTexts]);

    return (
        <div className="question-container">
            <div className="question-header">
                <button className="back-button"
                    onClick={onBackClick}
                    onMouseEnter={handleMouseEnter}
                    onMouseLeave={handleMouseLeave}
                >
                    <img src={iconSrc} alt="Back" />
                </button>
                <div className="question-number">Вопрос {questionNumber}</div>
            </div>
            <div className="question-text">
                <AnimatedText
                    text={questionText}
                    onComplete={handleAnimationComplete}
                />
            </div>
            <div className="button-container">
                {buttonTexts.map((text, index) => (
                    index <= currentButtonIndex && (
                        <button key={index} className="answer-button">
                            {text}
                        </button>
                    )
                ))}
            </div>
        </div>
    );
};

export default Question;
