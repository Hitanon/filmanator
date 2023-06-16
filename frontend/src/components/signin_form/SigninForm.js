import React, { useState } from "react";
import './style.css';


const SigninForm = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);

    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleShowPasswordClick = () => {
        setShowPassword(!showPassword);
    };

    return (
        <div className="sign-form">
            <form>
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