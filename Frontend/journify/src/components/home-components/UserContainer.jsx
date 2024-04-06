import UserInfo from "./UserInfo";
import UserStatistics from "./UserStatistics";
const UserContainer = () => {

    return (
        <div className="user-container">
            <UserInfo/>
            <UserStatistics/>
        </div>
    );
}
export default UserContainer;