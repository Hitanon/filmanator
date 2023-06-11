import About from "../pages/About";
import Home from "../pages/Home";
import PersonalData from "../pages/PersonalData";
import PrivacyPolicy from "../pages/PrivacyPolicy";
import Questionnaire from "../pages/Questionnaire";
import {
    HOME_ROUTE,
    QUESTIONNAIRE_ROUTE,
    PRIVACY_POLICY_ROUTE,
    PERSONAL_DATA_ROUTE,
    ABOUT_ROUTE
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
];
