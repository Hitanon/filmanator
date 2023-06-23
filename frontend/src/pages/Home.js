import React, { useEffect } from "react";
import Footer from "../components/footer/Footer";
import Navbar from "../components/navbar/Navbar";
import TextButton from "../components/home_textbutton/TextButton";

const handleMouseMove = (event) => {
    const x = (event.clientX / window.innerWidth) * 2 - 1;
    const y = (event.clientY / window.innerHeight) * 2 - 1;
    const homePageElement = document.querySelector('.home-page');
    if (homePageElement) {
        homePageElement.style.backgroundPosition = `${50 + x * 10}% ${50 + y * 10}%`;
    }
};

const Home = () => {

    useEffect(() => {
        document.addEventListener('mousemove', handleMouseMove);
        return () => {
            document.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    return (
        <div className="home-page">
            <Navbar />
            <div className="image-container">
                <img className="filmanator-main-image" src="/img/filmanator_main.webp" alt="main filmanator" />
                <TextButton />
            </div>
            <Footer />
        </div>
    );
}

export default Home;
