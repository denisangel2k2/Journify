import { Button } from "react-bootstrap";
const LoginButton = () => {
    const handleLogin = () => {
        window.location.href='http://localhost:8888/login';
    };
    return (
        <Button onClick={handleLogin} variant="default" className="login-btn">
            Login with Spotify
        </Button>
    );

};
export default LoginButton;