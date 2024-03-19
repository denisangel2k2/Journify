import React from 'react';

const Login = () => {
    const handleLogin = () => {
        window.location.href='http://localhost:8888/login';
    };
    
    return (
        <div>
            <button onClick={handleLogin}>Login with Spotify</button>
        </div>
    );
}

export default Login;