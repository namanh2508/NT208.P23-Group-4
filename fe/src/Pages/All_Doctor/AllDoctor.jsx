import Footer from "../../Components/Footer/Footer"
import Navbar from "../../Components/Navbar/Navbar"
import "./AllDoctor.css"
import { getDoctors } from "../../Components/api"
import doctor1 from "../../assets/doctor1.png"
import { useNavigate } from "react-router-dom"
import { useState, useEffect } from "react";
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const AllDoctor = ({ isAuthenticated }) => {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDoctors = async () => {
      const doctorData = await getDoctors();
      console.log("Doctors data:", doctorData);
      setDoctors(doctorData);
      setLoading(false);
    };

    fetchDoctors();
  }, []);

  const handleGetAdviceNow = (doctorId) => {
    console.log("Navigating to doctor with ID:", doctorId);  
    navigate(`/appointments/${doctorId}`); 
  };
  return (
    <div>
      <div className='navbar1'>
        <Navbar isAuthenticated={isAuthenticated}/>
      </div>
      <div className="doctor">
            <h2>Our Doctors</h2>
            {loading ? (
              <p>Loading...</p>
            ) : (
              <div className="contains">
                {doctors.slice(0, 10).map((doctor) => (
                  <div className="contain" key={doctor.id}>
                    <div className="img">
                    <img
                  src={doctor.profile_pic ? `${doctor.profile_pic.replace(/^\/+/, '')}` : doctor1}
                  alt={doctor.full_name}
                  />
                    </div>
                    <h4>{doctor.full_name}</h4>
                    <p>{doctor.department}</p>
                    <button onClick={() => handleGetAdviceNow(doctor.id)}>
                      Get advice now
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
      <Footer/>
    </div>
  )
}

export default AllDoctor
