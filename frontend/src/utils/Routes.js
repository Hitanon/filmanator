import About from "../pages/About";
import Home from "../pages/Home";
import PersonalAccount from "../pages/PersonalAccount";
import PersonalData from "../pages/PersonalData";
import PrivacyPolicy from "../pages/PrivacyPolicy";
import Questionnaire from "../pages/Questionnaire";
import Result from "../pages/Result";
import Signin from "../pages/Signin"

import {
    HOME_ROUTE,
    QUESTIONNAIRE_ROUTE,
    RESULT_ROUTE,
    PRIVACY_POLICY_ROUTE,
    PERSONAL_DATA_ROUTE,
    ABOUT_ROUTE,
    SIGNIN_ROUTE,
    PERSONAL_ACCOUNT
} from "./Consts";

export const publicRoutes = [
    {
        path: HOME_ROUTE,
        element: <Home />,
    },
    {
        path: QUESTIONNAIRE_ROUTE,
        element: <Questionnaire />,
    },
    {
        path: PRIVACY_POLICY_ROUTE,
        element: <PrivacyPolicy />,
    },
    {
        path: PERSONAL_DATA_ROUTE,
        element: <PersonalData />,
    },
    {
        path: ABOUT_ROUTE,
        element: <About />,
    },
    {
        path: RESULT_ROUTE,
        element: <Result/>,
    },
    {
        path: SIGNIN_ROUTE,
        element: <Signin/>,
    }
];

export const privateRoutes = [
    {
      path: PERSONAL_ACCOUNT,
      element: <PersonalAccount />,
    },
  ];
