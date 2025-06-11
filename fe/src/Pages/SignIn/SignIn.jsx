import { useState } from "react";
import api from "../../Components/api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../constant";
import "./Signin.css"; // Import CSS

function SigninPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            const res = await api.post("/api/token/", { username, password });
            
            localStorage.setItem(ACCESS_TOKEN, res.data.access);
            localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
            navigate("/");
            setTimeout(() => {
                window.location.reload(); 
            }, 100);
            
        } catch (error) {
            alert(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="form-container">
            <form onSubmit={handleSubmit}>
                <h1>SignIn</h1>
                <input
                    className="form-input"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                />
                <input
                    className="form-input"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                />
                {loading && <div className="loading">Loading...</div>}
                <button className="form-button" type="submit">
                    SignIn
                </button>
                <p className="signup-link">
                    Chưa có tài khoản? <span onClick={() => navigate("/register")} className="signup-link-text">Đăng ký</span>
                </p>
            </form>
        </div>
    );
}

export default SigninPage;
