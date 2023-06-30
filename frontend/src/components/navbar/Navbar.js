import React from "react";
import { Link } from 'react-router-dom';
import { observer } from "mobx-react-lite";

import styles from './style.css'
import { HOME_ROUTE } from "../../utils/Consts";




const Navbar = observer(() => {
    return (
        <nav className={styles.nav}>
            <Link to={HOME_ROUTE} className="logo-link">
                <img src="/img/filmanator_logo.svg" alt="Filmanator" />
            </Link>
        </nav>
    );
})

export default Navbar;