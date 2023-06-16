import React, { useEffect } from "react";
import TransparentNavbar from "../components/transparent_navbar/TransparentNavbar";
import SigninForm from "../components/signin_form/SigninForm";
import AgreementText from "../agreement_text/Agreement_text";


const Signin = () => {

    useEffect(() => {
        document.body.classList.add("signin-page");
        return () => {
            document.body.classList.remove("signin-page");
        };
    }, []);

    return (
        <>
            <TransparentNavbar />
            <div className="signin-body">
                <SigninForm />
                <AgreementText/>
            </div>
        </>
    );
}

export default Signin;
