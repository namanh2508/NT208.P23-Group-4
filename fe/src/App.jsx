import HomePage from "./Pages/HomePage"
import SigninPage from "./Pages/SignIn/SignIn"
import SignupPage from "./Pages/SignUp/SignUp"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import ProtectedRoute from "./Components/ProtectedRoute"
import NotFound from "./Pages/NotFound/NotFound"
import { useEffect, useState } from "react"
import { ACCESS_TOKEN } from "./constant"
import AppointmentPage from './Pages/Appointment/Appointment'
import AllDoctor from "./Pages/All_Doctor/AllDoctor"
import ProfilePage from "./Pages/Profile/Profile"
function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <SignupPage />
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    setIsAuthenticated(!!token);
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage isAuthenticated={isAuthenticated}/>} />
        <Route path="/login" element={<SigninPage />} />
        <Route
          path="/protected"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <h2>Trang chỉ dành cho người đã đăng nhập</h2>
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<NotFound isAuthenticated={isAuthenticated}/>} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="/logout" element={<Logout />} />  
        <Route path="/doctor" element={<AllDoctor isAuthenticated={isAuthenticated}/>} />    
        <Route path="/appointments/:doctorId" element={<AppointmentPage isAuthenticated={isAuthenticated}/>} />
        <Route path="/profile" element={<ProfilePage isAuthenticated={isAuthenticated}/>} />
        </Routes>
    </BrowserRouter>
  );
}

export default App
