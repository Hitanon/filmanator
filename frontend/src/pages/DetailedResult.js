import React, { useEffect } from "react";
import Footer from "../components/footer/Footer";
import Navbar from "../components/navbar/Navbar";
import DetailedFilmInfo from "../components/detailed_film_info/DetailedFilmInfo";

const DetailedResult = () => {
  useEffect(() => {
    document.body.classList.add("show-scrollbar");
    return () => {
      document.body.classList.remove("show-scrollbar");
    };
  }, []);

  return (
    <div className="detailed-result-page">
      <Navbar />
      <DetailedFilmInfo />
      <Footer />
    </div>
  );
};

export default DetailedResult;
