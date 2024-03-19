import React, { useEffect } from 'react';

const AuthCallbackPage = () => {

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const accessToken = urlParams.get('access_token');
        const expiresIn = urlParams.get('expires_in');

        if (accessToken) {
            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('expiresIn', expiresIn);
        }
        window.location.href = '/home';

    }, []);

    return (
        <div>
            <p>Redirecting...</p>
        </div>
    );
};

export default AuthCallbackPage;
