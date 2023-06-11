import React from "react";
import { Link } from 'react-router-dom';
import styles from './style.css';
import {PRIVACY_POLICY_ROUTE, PERSONAL_DATA_ROUTE, ABOUT_ROUTE} from "../../utils/Consts";

const Footer = () => {
    return ( 
        <footer className={styles.footer}>
            <Link to={PRIVACY_POLICY_ROUTE}>Политика конфиденциальности</Link>
            <Link to={PERSONAL_DATA_ROUTE}>Соглашение на обработку персональных данных</Link>
            <Link to={ABOUT_ROUTE}>© 2023 Filmanator - All rights reserved</Link>
        </footer>
     );
}
 
export default Footer;