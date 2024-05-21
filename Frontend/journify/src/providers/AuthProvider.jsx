import React, { useMemo } from 'react';
import { useEffect } from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthContext = React.createContext();

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useLocalStorage("token", null);
    const [userInfo, setUserInfo] = useLocalStorage("userInfo", null);
    const [expiresAt, setExpiresAt] = useLocalStorage("expiresAt", null); 
    const [refreshToken, setRefreshToken] = useLocalStorage("refreshToken", null);

    const navigate = useNavigate();

    useEffect(() => {
        if (token) {
            navigate('/home');
        } else {
            navigate('/');
        }
    }, [token]); 

    const login = async (token,expires_at,refresh_token) => {
        
        setExpiresAt(expires_at);
        setRefreshToken(refresh_token);
        setToken(token);
        await fetchUserInfo(token);
        navigate('/home');
    };
    const logout = () => {
        setToken(null);
        setUserInfo(null);
        navigate('/');
    };

    const fetchUserInfo = async (token) => {
        try {
            const response = await fetch('http://localhost:8888/user', {
                headers: {
                    'Authorization': `${token}`
                }
            });
            const data = await response.json();
            await setUserInfo(data);
        } catch (error) {
            console.error('Error fetching user info:', error);
        }

    };

    const sharedValues = useMemo(() => {
        return {
            token,
            setToken,
            setExpiresAt,
            expiresAt,
            refreshToken,
            setRefreshToken,
            login,
            logout,
            userInfo
        };
    }, [token, userInfo]);

    return <AuthContext.Provider value={sharedValues}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
    const context = React.useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

export const useLocalStorage = (keyName, defaultValue) => {
    const [storedValue, setStoredValue] = useState(() => {
        try {
            const value = window.localStorage.getItem(keyName);
            if (value) {
                return JSON.parse(value);
            } else {
                window.localStorage.setItem(keyName, JSON.stringify(defaultValue));
                return defaultValue;
            }
        } catch (err) {
            return defaultValue;
        }
    });
    const setValue = (newValue) => {
        try {
            window.localStorage.setItem(keyName, JSON.stringify(newValue));
        } catch (err) {
        }
        setStoredValue(newValue);
    };
    return [storedValue, setValue];
};