import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";


import './style.css';
import { Context } from "../../index";
import { login } from '../../services/AuthService';
import { HOME_ROUTE } from "../../utils/Consts";


const SigninForm = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();
    const { user } = useContext(Context);


    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleShowPasswordClick = () => {
        setShowPassword(!showPassword);
    };

    const handleFormSubmit = async (event) => {
        event.preventDefault();
        try {
            const data = await login(email, password);
            localStorage.setItem('accessToken', data.access);
            localStorage.setItem('refreshToken', data.refresh);
            user.setIsAuth(true);
            setErrorMessage('');
            navigate(HOME_ROUTE);
        } catch (error) {
            setErrorMessage(error.message);
        }
    };

    return (
        <div className="sign-form">
            <form onSubmit={handleFormSubmit} >
                <h1>Вход</h1>
                <div className="input-container">
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={handleEmailChange}
                    />
                </div>
                <div className="input-container">
                    <div className="password-input-container">
                        <input
                            type={showPassword ? "text" : "password"}
                            placeholder="Пароль"
                            value={password}
                            onChange={handlePasswordChange}
                        />
                        <button type="button" onClick={handleShowPasswordClick}>
                            {showPassword ? (
                                <img src="/img/hide_password_icon.png" alt="Hide password" />
                            ) : (
                                <img src="/img/show_password_icon.png" alt="Show password" />
                            )}
                        </button>
                    </div>
                </div>
                {errorMessage && <div className="error-message">{errorMessage}</div>}
                <div className="links">
                    <a href="/">Не помню пароль</a>
                    <a href="/">Создать аккаунт</a>
                </div>
                <button type="submit" className="submit">
                    Войти
                </button>
            </form>
        </div>
    );
}

export default SigninForm;