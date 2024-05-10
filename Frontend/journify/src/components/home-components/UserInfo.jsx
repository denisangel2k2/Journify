import React, { useEffect, useState } from 'react';
import { useAuth } from '../../providers/AuthProvider';
import LogoutIcon from '@mui/icons-material/Logout';
const UserInfo = () => {
    const { userInfo } = useAuth();

    if (!userInfo) {
        return null;
    }
    return (
        <div className='user-information'>
            <img src={userInfo['images']} className='user-picture'></img>

            <div className='user-profile-text'>
                <div id='name-and-logout'>
                    <p id='display-name'>{userInfo['display_name']}</p>
                    <LogoutIcon className='logout-button' onClick={
                        () => {
                            localStorage.clear();
                            window.location.reload();
                        }
                    }>Logout</LogoutIcon>

                </div>
                <p id='follower-count'>{userInfo['followers']} Followers</p>

            </div>



        </div >
    );
};
export default UserInfo;
