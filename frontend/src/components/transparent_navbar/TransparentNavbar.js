import React from "react";
import { Link, useNavigate  } from "react-router-dom";

import "./styles.css";
import { HOME_ROUTE } from "../../utils/Consts";

const TransparentNavbar = () => {
  const navigate = useNavigate();

  const handleSigninClick = () => {
    navigate(-1);
  };

  return (
    <nav className={"nav"}>
      <Link to={HOME_ROUTE} className="logo-link">
        <img src="/img/filmanator_logo.svg" alt="Filmanator" />
      </Link>
      <button onClick={handleSigninClick} className="close-button">
        <img src="/img/close_button.svg" alt="close" />
      </button>
    </nav>
  );
};

export default TransparentNavbar;
