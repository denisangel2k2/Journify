import React, { useEffect } from 'react';
import { useAuth } from '../providers/AuthProvider';
const AuthCallbackPage = () => {
    const { login, } = useAuth();
    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const accessToken = urlParams.get('access_token');
        const expiresAt = urlParams.get('expires_at');
        const refreshToken = urlParams.get('refresh_token');

        if (accessToken) {
            login(accessToken, expiresAt, refreshToken); 
            // localStorage.setItem('expiresIn', expiresIn);
            // localStorage.setItem('refreshToken', refreshToken);
        }
    }, []);

    return (
        <div>
            <p>Redirecting...</p>
        </div>
    );
};

export default AuthCallbackPage;
