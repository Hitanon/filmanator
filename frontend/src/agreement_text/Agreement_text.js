import React from "react";
import "./style.css"
import { PRIVACY_POLICY_ROUTE, PERSONAL_DATA_ROUTE } from "./../utils/Consts";

const AgreementText = () => {
    return (
        <div className="agreement-text">
            <div>Авторизуясь, ты соглашаешься с условиями</div>
            <div>
                <a href={PERSONAL_DATA_ROUTE}>Пользовательского соглашения</a> и{" "}
                <a href={PRIVACY_POLICY_ROUTE}>Политики конфиденциальности</a>
            </div>
        </div>
    );
};

export default AgreementText;