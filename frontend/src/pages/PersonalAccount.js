import React, { useEffect } from "react";

import TransparentNavbar from "../components/transparent_navbar/TransparentNavbar";
import UserProfile from "../components/user_profile/UserProfile";

const PersonalAccount = () => {
    useEffect(() => {
        document.body.classList.add("personal-account-page");
        return () => {
            document.body.classList.remove("personal-account-page");
        };
    }, []);
    return (
        <>
            <TransparentNavbar />
            <UserProfile />
        </>
    );
}

export default PersonalAccount;