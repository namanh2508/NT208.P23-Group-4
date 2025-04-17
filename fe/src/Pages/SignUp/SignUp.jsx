import { useState } from "react";
import api from "../../Components/api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../constant";
import "./SignUp.css";

function SignupPage() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [address, setAddress] = useState("");
  const [mobile, setMobile] = useState("");
  const [profilePic, setProfilePic] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append("first_name", firstName);
    formData.append("last_name", lastName);
    formData.append("email", email);
    formData.append("username", username);
    formData.append("password", password);
    formData.append("address", address);
    formData.append("mobile", mobile);
    if (profilePic) formData.append("profile_pic", profilePic);

    try {
      const res = await api.post("/api/patient/register/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      localStorage.setItem(ACCESS_TOKEN, res.data.access);
      localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
      navigate("/");
      setTimeout(() => window.location.reload(), 100);
    } catch {
      alert("Sign Up failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <h1>Sign Up</h1>
      <input
        className="form-input"
        type="text"
        value={firstName}
        onChange={(e) => setFirstName(e.target.value)}
        placeholder="First Name"
      />
      <input
        className="form-input"
        type="text"
        value={lastName}
        onChange={(e) => setLastName(e.target.value)}
        placeholder="Last Name"
      />
      <input
        className="form-input"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
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
      <input
        className="form-input"
        type="text"
        value={address}
        onChange={(e) => setAddress(e.target.value)}
        placeholder="Address"
      />
      <input
        className="form-input"
        type="text"
        value={mobile}
        onChange={(e) => setMobile(e.target.value)}
        placeholder="Mobile"
      />
      <input
        className="form-input"
        type="file"
        accept="image/*"
        onChange={(e) => setProfilePic(e.target.files[0])}
        placeholder="Profile Picture"
      />
      {loading && <div>Loading...</div>}
      <button className="form-button" type="submit">
        Sign Up
      </button>

      {/* Dòng chữ chuyển hướng đến trang đăng nhập */}
      <p className="signin-link">
        Đã có tài khoản?{" "}
        <span onClick={() => navigate("/login")} className="signin-link-text">
          Đăng nhập
        </span>
      </p>
    </form>
  );
}

export default SignupPage;
