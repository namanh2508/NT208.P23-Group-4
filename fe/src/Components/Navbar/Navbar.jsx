import './Navbar.css';
import chevron from "../../assets/chevron-down.svg";
import account from "../../assets/account.svg";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Navbar = ({ isAuthenticated }) => {
  const navigate = useNavigate();
  const [showDropdown, setShowDropdown] = useState(false);
  const handleLogout = () => {
    navigate("/logout");
  };
  const toggleDropdown = () => {
    setShowDropdown(prev => !prev);
  };
  return (
    <div className='nav'>
      <div className='nav-logo'>HospitAI</div>
      <ul className='nav-menu'>
        <li onClick={() => navigate("/")}>Home</li>
        <li onClick={() => navigate("/about")}>About</li>
        <li className='nav-service'>
          Service <img src={chevron} alt="dropdown icon" />
          <ul className="dropdown">
            <li onClick={() => navigate("/ai-support")}>AI Support</li>
            <li onClick={() => navigate("/book-appointment")}>Book an Appointment</li>
            <li onClick={() => navigate("/drug-info")}>Drug Information</li>
            <li onClick={() => navigate("/talk-to-doctor")}>Talk to a Doctor</li>
          </ul>
        </li>
        <li onClick={() => navigate("/doctor")}>Doctor</li>
        {!isAuthenticated && (
          <li className='nav-signin' onClick={() => navigate("/login")}>Sign In</li>
        )}
        {isAuthenticated && (
          <li className="nav-account">
            <img
              src={account}
              alt="Account"
              className="account-icon"
              onClick={toggleDropdown}
            />
            {showDropdown && (
              <ul className="account-dropdown">
                <li onClick={() => { navigate("/profile"); setShowDropdown(false); }}>Thông tin cá nhân</li>
                <li onClick={() => { handleLogout(); setShowDropdown(false); }}>Đăng xuất</li>
              </ul>
            )}
          </li>
        )}
      </ul>      
    </div>
  );
}

export default Navbar;
