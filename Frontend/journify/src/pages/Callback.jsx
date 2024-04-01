import React, { useEffect } from 'react';
import { useAuth } from '../providers/AuthProvider';
const AuthCallbackPage = () => {
    const { login } = useAuth();
    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const accessToken = urlParams.get('access_token');
        const expiresIn = urlParams.get('expires_in');

        if (accessToken) {
            // localStorage.setItem('accessToken', accessToken);
            login(accessToken);
            localStorage.setItem('expiresIn', expiresIn);
        }
        //window.location.href = '/home';

    }, []);

    return (
        <div>
            <p>Redirecting...</p>
        </div>
    );
};

export default AuthCallbackPage;
