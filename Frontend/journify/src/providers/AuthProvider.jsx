import React, { useMemo } from 'react';
import { useEffect } from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthContext = React.createContext();

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useLocalStorage("token", null);
    const navigate = useNavigate();

    useEffect(() => {
        if (token) {
            navigate('/home');
        } else {
            navigate('/');
        }
    }, [token]); // might need to remove token from here

    const login = (token) => {
        console.log(token);
        setToken(token);
        navigate('/home');
    };
    const logout = () => {
        setToken(null);
        navigate('/');
    };

    const sharedValues = useMemo(() => {
        return {
            token,
            login,
            logout
        };
    }, [token]);

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
                if (window.localStorage.getItem("expiresIn") > 0) {
                    return defaultValue;
                }
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