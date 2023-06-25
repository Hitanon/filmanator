import React, { useState } from 'react';

import './style.css';
import SquareButtonBig from '../square_button_big/SquareButtonBig';

const BIG_SQUARE_BUTTON_SIZE = "70px";

const SharePopup = ({ title, link, isSeries, onClose }) => {
    const [isLinkCopied, setIsLinkCopied] = useState(false);

    const handleVKShare = () => {
        window.open(`https://vk.com/share.php?url=${encodeURIComponent(link)}&title=${encodeURIComponent(title)}`);
        onClose();
    };

    const handleTelegramShare = () => {
        window.open(`https://t.me/share/url?url=${encodeURIComponent(link)}&text=${encodeURIComponent(title)}`);
        onClose();
    };

    const handleCopyLink = () => {
        navigator.clipboard.writeText(link);
        setIsLinkCopied(true);
        setTimeout(onClose, 1000);
    };

    return (
        <div className="share-popup">
            <button className="close-share-button" onClick={onClose}>
                <img src="/img/close_button.svg" alt="Forward" />
            </button>
            <h3>{isSeries ? 'Поделиться сериалом' : 'Поделиться фильмом'}</h3>
            <h3>"{title}"</h3>
            <div className='share-buttons-container'>
                <SquareButtonBig onClick={handleVKShare} icon="/img/vk_icon.svg" size={BIG_SQUARE_BUTTON_SIZE} alt_text="vkontakte"/>
                <SquareButtonBig onClick={handleTelegramShare} icon="/img/telegram_icon.svg" size={BIG_SQUARE_BUTTON_SIZE} alt_text="telegram"/>
                <SquareButtonBig onClick={handleCopyLink} icon="/img/copy_icon.svg" size={BIG_SQUARE_BUTTON_SIZE} alt_text="clipboard"/>
            </div>
            {isLinkCopied && <p className='copy-link'>Ссылка скопирована!</p>}
        </div>
    );
};

export default SharePopup;
