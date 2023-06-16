import React, { useState } from 'react';
import { observer } from 'mobx-react-lite';

import './style.css';
import userStore from '../../store/UserStore';

const UserButtons = observer(() => {
  const [activeButton, setActiveButton] = useState(userStore.active_tab);

  const handleButtonClick = (button) => {
    setActiveButton(button);
    userStore.setActiveTab(button);
  };

  return (
    <div className="button-group">
      <button
        className={`button ${activeButton === 'history' ? 'active' : ''}`}
        onClick={() => handleButtonClick('history')}
      >
        История
      </button>
      <button
        className={`button ${activeButton === 'likes' ? 'active' : ''}`}
        onClick={() => handleButtonClick('likes')}
      >
        Понравившиеся
      </button>
      <button
        className={`button ${activeButton === 'blacklist' ? 'active' : ''}`}
        onClick={() => handleButtonClick('blacklist')}
      >
        Черный список
      </button>
    </div>
  );
});

export default UserButtons;
