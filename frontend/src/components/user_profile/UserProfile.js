import React from "react";
import { observer } from 'mobx-react-lite';
import userStore from '../../store/UserStore';

import './style.css';
import UserIcon from "../uer_icon/UserIcon";
import UserButtons from "../user_buttons/UserButtons";

const handleEditEmail = () => {
    console.log("pressed edit email")
};

const UserProfile = observer(() => {
    return (
        <div className="user-profile-container">
            <UserIcon email={userStore.email} onEmailClick={handleEditEmail}/>
            <UserButtons/>
        </div>
    );
});

export default UserProfile;