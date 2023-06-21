import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from "react-router-dom";

import { observer} from 'mobx-react-lite';
import { reaction } from 'mobx';
import './style.css'
import AnimatedText from '../animated_text/AnimatedText';
import questionStore from '../../store/QuestionStore';

import {RESULT_ROUTE} from "../../utils/Consts";

const handleMouseEnter = (setIconSrc) => {
    setIconSrc('/img/previous_question_button_active.svg');
};

const handleMouseLeave = (setIconSrc) => {
    setIconSrc('/img/previous_question_button.svg');
};

const handleButtonClick = async (answerId) => {
    questionStore.submitAnswer(answerId);
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
    const navigate = useNavigate();

    const handleAnimationComplete = useCallback(() => {
        setIsTextAnimated(true);
    }, []);


    useEffect(() => {
        updateCurrentButtonIndex(isTextAnimated, currentButtonIndex, setCurrentButtonIndex);
    }, [isTextAnimated, currentButtonIndex]);

    useEffect(() => {
        questionStore.fetchQuestion();
    }, []);


    useEffect(() => {
        const disposer = reaction(
            () => questionStore.isComplete,
            (isComplete) => {
                if (isComplete) {
                    navigate(RESULT_ROUTE);
                }
            }
        );
        return () => disposer();
    }, [navigate]);

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
                {questionStore.question && (
                    <AnimatedText
                        text={questionStore.question}
                        onComplete={handleAnimationComplete}
                    />
                )}
            </div>
            <div className="button-container">
                {questionStore.answers.map((answer) => (
                    <button key={answer.id} className="answer-button" onClick={() => handleButtonClick(answer.id)}>
                        {answer.body}
                    </button>
                ))}
            </div>
        </div>
    );
});

export default Question;
