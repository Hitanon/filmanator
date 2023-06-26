import React, { useContext, useState } from "react";
import { Link, useNavigate } from 'react-router-dom';
import { observer } from "mobx-react-lite";

import styles from './style.css'
import { Context } from "../../index";
import { HOME_ROUTE, SIGNIN_ROUTE } from "../../utils/Consts";


const handleIconEnter = (setIconSrc) => {
    setIconSrc('/img/personal_acc_btn_active.svg');
};

const handleIconLeave = (setIconSrc) => {
    setIconSrc('/img/personal_acc_btn.svg');
};

const Navbar = observer(() => {
    const navigate = useNavigate();
    const { user } = useContext(Context);
    const [iconSrc, setIconSrc] = useState('/img/personal_acc_btn.svg');

    const handleSigninClick = () => {
        navigate(SIGNIN_ROUTE)
    };


    return (
        <nav className={styles.nav}>
            <Link to={HOME_ROUTE} className="logo-link">
                <img src="/img/filmanator_logo.svg" alt="Filmanator" />
            </Link>
            {
                user.isAuth
                    ?
                    <button
                        onClick={handleSigninClick}
                        className="personal-acc-btn"
                        onMouseEnter={() => handleIconEnter(setIconSrc)}
                        onMouseLeave={() => handleIconLeave(setIconSrc)}>
                        <img className="Icon-button" src={iconSrc} alt="Personal account" />
                    </button>
                    :
                    <button onClick={handleSigninClick}>
                        ВОЙТИ
                    </button>
            }
        </nav>
    );
})

export default Navbar;