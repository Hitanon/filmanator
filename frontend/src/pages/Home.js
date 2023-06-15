import React, { useEffect } from "react";
import {addBodyClass, removeBodyClass} from "../utils/BodyClassLoader";
import Footer from "../components/footer/Footer";
import Navbar from "../components/navbar/Navbar";
import TextButton from "../components/home_textbutton/TextButton";

const handleMouseMove = (event) => {
    const x = (event.clientX / window.innerWidth) * 2 - 1;
    const y = (event.clientY / window.innerHeight) * 2 - 1;
    document.body.style.backgroundPosition = `${50 + x * 10}% ${50 + y * 10}%`;
};


const Home = () => {

    useEffect(() => {
        addBodyClass('home-bg');
        document.addEventListener('mousemove', handleMouseMove);
        return () => {
            removeBodyClass('homge-bg');
            document.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    return (
        <>
            <Navbar />
            <div className="image-container">
                <img className="filmanator-main-image" src="/img/filmanator_main.png" alt="main filmanator" />
                <TextButton />
            </div>
            <Footer />
        </>
    );
}

export default Home;
