import React from "react";
import { Link } from 'react-router-dom';
import styles from './style.css'
import {HOME_ROUTE} from "../../utils/Consts";

const Navbar = () => {
    return (
        <nav className={styles.nav}>
            <Link to={HOME_ROUTE} className="logo-link">
                <img src="/img/filmanator_logo.svg" alt="Filmanator" />
            </Link>
            <button>
                ВОЙТИ
            </button>
        </nav>
    );
}

export default Navbar;