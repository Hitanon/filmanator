import React, { useEffect } from "react";
import Footer from "../components/footer/Footer";
import Navbar from "../components/navbar/Navbar";
import TextButton from "../components/home_textbutton/TextButton";


const Home = () => {

    useEffect(() => {
        const handleMouseMove = (event) => {
            const x = (event.clientX / window.innerWidth) * 2 - 1;
            const y = (event.clientY / window.innerHeight) * 2 - 1;
            document.body.style.backgroundPosition = `${50 + x * 10}% ${50 + y * 10}%`;
        };

        document.addEventListener('mousemove', handleMouseMove);
        return () => {
            document.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    useEffect(() => {
        document.body.classList.add('homepage');
        return () => {
            document.body.classList.remove('homepage');
        }
    }, []);



    return (
        <>
            <Navbar />
            <div className="image-container">
                <img className="filmanator-main-image" src="/img/filmanator_main.png" alt="main image of filmanator" />
                <TextButton />
            </div>
            <Footer />
        </>
    );
}

export default Home;