import './Navbar.css';
import chevron from "../../assets/chevron-down.svg";
import { useNavigate } from "react-router-dom";

const Navbar = ({ isAuthenticated }) => {
  const navigate = useNavigate();

  return (
    <div className='nav'>
      <div className='nav-logo'>HospitAI</div>
      <ul className='nav-menu'>
        <li onClick={() => navigate("/")}>Home</li>
        <li onClick={() => navigate("/about")}>About</li>
        <li className='nav-service'>
          Service <img src={chevron} alt="dropdown icon" />
          <ul className="dropdown">
            <li onClick={() => navigate("/chatbot")}>AI Support</li>
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
          <li className='nav-signin' onClick={() => navigate("/logout")}>Logout</li>
        )}
      </ul>      
    </div>
  );
}

export default Navbar;
