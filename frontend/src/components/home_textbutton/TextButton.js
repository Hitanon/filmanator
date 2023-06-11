import React from "react";
import { useNavigate } from "react-router-dom";
import './style.css';
import {QUESTIONNAIRE_ROUTE} from "../../utils/Consts";

const TextButton = () => {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate(QUESTIONNAIRE_ROUTE)
    }
    return (
        <div className="text-button">
            <h1 className='text-button-heading'>
                Привет, я - Filmanator, помощник по подбору фильмов и сериалов. Ответь на несколько вопросов и я подскажу тебе, что посмотреть сегодня. Начинаем?
            </h1>
            <button onClick={handleClick} className="start-button">
                Начать опрос
            </button>
        </div>
    );
}

export default TextButton;