import React from "react";
import styles from './style.css'

const Footer = () => {
    return ( 
        <footer className={styles.footer}>
            <a href="/privacy_policy">Политика конфиденциальности</a>
            <a href="/personal_data_processing_agreement">Соглашение на обработку персональных данных</a>
            <a href="/about">© 2023 Filmanator - All rights reserved</a>
        </footer>
     );
}
 
export default Footer;