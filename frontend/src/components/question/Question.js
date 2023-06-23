import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from "react-router-dom";
import { CircularProgress } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';

import { observer } from 'mobx-react-lite';
import { reaction } from 'mobx';

import './style.css'
import AnimatedText from '../animated_text/AnimatedText';
import questionStore from '../../store/QuestionStore';

import { RESULT_ROUTE } from "../../utils/Consts";


const updateCurrentButtonIndex = (isTextAnimated, currentButtonIndex, setCurrentButtonIndex) => {
    if (isTextAnimated && currentButtonIndex < questionStore.answers.length - 1) {
        const timeout = setTimeout(() => {
            setCurrentButtonIndex(currentButtonIndex + 1);
        }, 100);
        return () => clearTimeout(timeout);
    }
};

const theme = createTheme({
    palette: {
        primary: {
            main: '#ffffff',
        },
    },
});

const Question = observer(() => {
    const [currentButtonIndex, setCurrentButtonIndex] = useState(-1);
    const [isTextAnimated, setIsTextAnimated] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleAnimationComplete = useCallback(() => {
        setIsTextAnimated(true);
    }, []);

    const handleButtonClick = async (answerId) => {
        setIsLoading(true);
        questionStore.submitAnswer(answerId).then(() => {
            setIsLoading(false);
        });
    };

    useEffect(() => {
        updateCurrentButtonIndex(isTextAnimated, currentButtonIndex, setCurrentButtonIndex);
    }, [isTextAnimated, currentButtonIndex]);

    useEffect(() => {

        setIsLoading(true);
        questionStore.fetchQuestion().then(() => {
            setIsLoading(false);
        });

        const disposer = reaction(
            () => questionStore.question,
            () => {
                setCurrentButtonIndex(-1);
            }
        );
        
        return () => disposer();
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
                <div className="question-number">Вопрос {questionStore.questionNumber}</div>
            </div>
            <div className="circular-progress-container" style={{ display: isLoading ? 'flex' : 'none' }}>
                <ThemeProvider theme={theme}>
                    <CircularProgress className="circular-progress-color" size={"6vw"} />
                </ThemeProvider>
            </div>
            <div className="content-container" style={{ opacity: isLoading ? 0.5 : 1 }}>
                <div className="question-text">
                    {questionStore.question && (
                        <AnimatedText text={questionStore.question} onComplete={handleAnimationComplete} />
                    )}
                </div>
                <div className="button-container">
                    {questionStore.answers
                        .slice(0, currentButtonIndex + 1)
                        .map((answer) => (
                            <button
                                key={answer.id}
                                className="answer-button"
                                onClick={() => handleButtonClick(answer.id)}
                                disabled={isLoading}
                            >
                                {answer.body}
                            </button>
                        ))}
                </div>
            </div>
        </div>



    );
});

export default Question;
