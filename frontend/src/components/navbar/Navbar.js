import React from "react";
import { Link, useNavigate } from 'react-router-dom';

import styles from './style.css'
import { HOME_ROUTE, SIGNIN_ROUTE } from "../../utils/Consts";




const Navbar = () => {
    const navigate = useNavigate();

    const handleSigninClick = () => {
        navigate(SIGNIN_ROUTE)
    };
    
    return (
        <nav className={styles.nav}>
            <Link to={HOME_ROUTE} className="logo-link">
                <img src="/img/filmanator_logo.svg" alt="Filmanator" />
            </Link>
            <button onClick={handleSigninClick}>
                ВОЙТИ
            </button>
        </nav>
    );
}

export default Navbar;