import MainTitle from "../shared/MainTitle";
import LoginButton from "./LoginButton";
import LoginCloud from "./LoginCloud";

const LoginModule = () => {
    return (
        <>
            <div class="login-module">
                <LoginCloud text={"Complete the musical journal!"}/>
                <MainTitle/>
                <h2>Musically express how you feel in certain situations and do not forget to share it with your friends!</h2>
                <LoginButton/>
            </div>
        </>
    )
}
export default LoginModule;