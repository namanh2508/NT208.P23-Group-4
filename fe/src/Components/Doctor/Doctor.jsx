import './Doctor.css';
import doctor1 from "../../assets/doctor1.png";
import { useState, useEffect } from "react";
import { getDoctors } from "../api";
import { useNavigate } from 'react-router-dom';


const Doctor = ({ isAuthenticated }) => {
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
    if (!isAuthenticated) {
      navigate("/login");
    } else {
    navigate(`/appointments/${doctorId}`);
    }
  };

  return (
    <div className="doctor">
      <div className='title'>
        <h2>Our Doctors</h2>
        <p onClick={() => navigate("/doctor")}>See more </p>
      </div>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="contains">
          {doctors.slice(0, 4).map((doctor) => (
            <div className="contain" key={doctor.id}>
              <div className="img">
              <img
            src={doctor.picture ? doctor.picture : doctor1}
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
  );
};

export default Doctor;
