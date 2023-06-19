import React from "react";
import Footer from "../components/footer/Footer";
import Navbar from "../components/navbar/Navbar";
import DetailedFilmInfo from "../components/detailed_film_info/DetailedFilmInfo";

const DetailedResult = () => {
    return (
        <div className="detailed-result-page">
            <Navbar />
            <DetailedFilmInfo />
            <Footer />
        </div>
    );
}

export default DetailedResult;