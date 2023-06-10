import React from "react";
import styles from './style.css'

const Navbar = () => {
    return (
        <nav className={styles.nav}>
            <a href="/" className="logo-link">
                <img src="/img/filmanator_logo.svg" alt="Filmanator" />
            </a>
            <button>
                ВОЙТИ
            </button>
        </nav>
    );
}

export default Navbar;