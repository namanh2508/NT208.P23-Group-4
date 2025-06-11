import { useState } from "react";
import api from "../../Components/api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../constant";
import "./SignUp.css";

function SignupPage() {
  const [form, setForm] = useState({
    username: "",
    password: "",
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    gender: "",
    birthday: "",
    family_phone: "",
    weight: "",
    height: "",
    description: "",
  });
  const [picture, setPicture] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    Object.entries(form).forEach(([key, value]) => {
      if (value !== "") formData.append(key, value);
    });
    if (picture) formData.append("picture", picture);

    try {
      const res = await api.post("/api/patient/register/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      localStorage.setItem(ACCESS_TOKEN, res.data.access);
      localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
      navigate("/");
      setTimeout(() => window.location.reload(), 100);
    } catch (err) {
      console.error("Signup error:", err.response?.data);
      alert("Sign Up failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <h1>Sign Up</h1>

      <input name="first_name" className="form-input" type="text" placeholder="First Name" value={form.first_name} onChange={handleChange} />
      <input name="last_name" className="form-input" type="text" placeholder="Last Name" value={form.last_name} onChange={handleChange} />
      <input name="email" className="form-input" type="email" placeholder="Email" value={form.email} onChange={handleChange} />
      <input name="username" className="form-input" type="text" placeholder="Username" value={form.username} onChange={handleChange} />
      <input name="password" className="form-input" type="password" placeholder="Password" value={form.password} onChange={handleChange} />
      <input name="phone" className="form-input" type="text" placeholder="Phone" value={form.phone} onChange={handleChange} />
      <select
        name="gender"
        className="form-input"
        value={form.gender}
        onChange={handleChange}
      >
        <option value="">Select Gender</option>
        <option value="nam">Male</option>
        <option value="nữ">Female</option>
        <option value="other">Other</option>
      </select>
      <input name="birthday" className="form-input" type="date" placeholder="Birthday" value={form.birthday} onChange={handleChange} />
      <input name="family_phone" className="form-input" type="text" placeholder="Family Phone" value={form.family_phone} onChange={handleChange} />
      <input name="weight" className="form-input" type="number" placeholder="Weight (kg)" value={form.weight} onChange={handleChange} />
      <input name="height" className="form-input" type="number" placeholder="Height (cm)" value={form.height} onChange={handleChange} />
      <input name="description" className="form-input" type="text" placeholder="Description" value={form.description} onChange={handleChange} />
      <input type="file" className="form-input" accept="image/*" onChange={(e) => setPicture(e.target.files[0])} />

      {loading && <div>Loading...</div>}
      <button className="form-button" type="submit">Sign Up</button>

      <p className="signin-link">
        Đã có tài khoản?{" "}
        <span onClick={() => navigate("/login")} className="signin-link-text">Đăng nhập</span>
      </p>
    </form>
  );
}

export default SignupPage;
