import Form from "../Components/Form";
import { useNavigate } from "react-router-dom";
const SigninPage = () => {
    const navigate = useNavigate();
    return (
    <div>
        <Form route="/api/token/" method="login"/>;
        <h1 onClick={() => navigate("/register")}>Click here to Sign Up</h1>
    </div>
    );
};

export default SigninPage;