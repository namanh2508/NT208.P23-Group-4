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
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDepartment, setSelectedDepartment] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDoctors = async () => {
      const doctorData = await getDoctors();
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

  const departments = [...new Set(doctors.map(d => d.department))];

  const filteredDoctors = doctors.filter(doctor =>
    doctor.full_name.toLowerCase().includes(searchTerm.toLowerCase()) &&
    (selectedDepartment ? doctor.department === selectedDepartment : true)
  );

  return (
    <div>
      <div className='navbar1'>
        <Navbar isAuthenticated={isAuthenticated}/>
      </div>

      <div className="doctor-page">
        <div className="sidebar">
          <h3>Filter</h3>
          <div className="search-box">
            <input
              type="text"
              placeholder="Search by name"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className="department-filter">
            <h4>Departments</h4>
            <button onClick={() => setSelectedDepartment('')} className={selectedDepartment === '' ? 'active' : ''}>All</button>
            {departments.map((dept, index) => (
              <button
                key={index}
                onClick={() => setSelectedDepartment(dept)}
                className={selectedDepartment === dept ? 'active' : ''}
              >
                {dept}
              </button>
            ))}
          </div>
        </div>

        <div className="doctor-list">
          <h2>Our Doctors</h2>
          {loading ? (
            <p>Loading...</p>
          ) : (
            <div className="contains">
              {filteredDoctors.map((doctor) => (
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
      </div>

      <Footer/>
    </div>
  )
}

export default AllDoctor
