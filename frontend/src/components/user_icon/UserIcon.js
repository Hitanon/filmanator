import React, { useState } from 'react';
import './style.css';

const UserIcon = ({ email, onEmailClick }) => {
  const [isHovering, setIsHovering] = useState(false);

  const handleMouseEnter = () => {
    setIsHovering(true);
  };

  const handleMouseLeave = () => {
    setIsHovering(false);
  };

  return (
    <div className="user-icon-container">
      <img src="/img/user_icon.svg" alt="User Icon" className="user-icon" />
      <div
        className="email-container"
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        <span
          className={`email ${isHovering ? 'hover' : ''}`}
          onClick={onEmailClick}
        >
          {email}
        </span>
        <img
          src={
            isHovering ? '/img/edit_email_icon_active.svg' : '/img/edit_email_icon.svg'
          }
          alt="Email Icon"
          className="email-icon"
          onClick={onEmailClick}
        />
      </div>
    </div>
  );
};

export default UserIcon;
