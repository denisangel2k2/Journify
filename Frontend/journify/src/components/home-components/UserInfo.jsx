import React, { useEffect, useState } from 'react';
import { useAuth } from '../../providers/AuthProvider';

const UserInfo = () => {
    const { userInfo } = useAuth();

    if (!userInfo) {
        return null; 
    }
    console.log(userInfo);
    return (
        <div className='user-information'>
            <img src={userInfo['images']} className='user-picture'></img>
            <div className='user-profile-text'>
                <p id='display-name'>{userInfo['display_name']}</p>
                <p id='follower-count'>{userInfo['followers']} Followers</p>
            </div>

        </div>
    );
};
export default UserInfo;
