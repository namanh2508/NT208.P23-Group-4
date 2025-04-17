import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { createAppointment, getDoctorById } from '../../Components/api';  
import './Appointment.css';
import Footer from "../../Components/Footer/Footer";
import Navbar from "../../Components/Navbar/Navbar";

const getAvailableSlots = () => {
  const slots = [];
  const now = new Date();

  for (let i = 0; i < 7; i++) {
    const date = new Date(now);
    date.setDate(now.getDate() + i);

    const daySlots = [];
    for (let hour = 10; hour < 17; hour++) {
      for (let minute = 0; minute < 60; minute += 30) {
        const time = new Date(date);
        time.setHours(hour, minute, 0);
        daySlots.push(time);
      }
    }
    slots.push({ date: date.toISOString().split('T')[0], daySlots });
  }

  return slots;
};

const AppointmentPage = ({ isAuthenticated }) => {
  const { doctorId } = useParams();
  const [doctorInfo, setDoctorInfo] = useState(null);
  const [appointmentData, setAppointmentData] = useState({
    appointmentDate: '',
    appointmentTime: '',
    description: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [availableSlots, setAvailableSlots] = useState([]);

  useEffect(() => {
    const fetchDoctor = async () => {
      try {
        const doctor = await getDoctorById(doctorId);
        setDoctorInfo(doctor);
      } catch (error) {
        console.error("Error fetching doctor info:", error);
      }
    };
    fetchDoctor();
    
    setAvailableSlots(getAvailableSlots());
  }, [doctorId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setAppointmentData(prevState => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await createAppointment(doctorId, appointmentData);
      console.log('Appointment created:', data);
    } catch (error) {
      console.error('Error creating appointment:', error);
      setError('Failed to create appointment. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="appointment-page">
      <div className='navbar1'>
        <Navbar isAuthenticated={isAuthenticated}/>
      </div>
      <div className="appointment-container">
        <h2>Create Appointment with Doctor</h2>

        {doctorInfo && (
          <div className="doctor-info-container">
            <div className="doctor-avatar-container">
              <img
                src={doctorInfo.profile_pic ? doctorInfo.profile_pic.replace(/^\/+/, '') : '/default-doctor.png'}
                alt={doctorInfo.full_name}
                className="doctor-avatar"
              />
            </div>
            <div className="doctor-info">
              <h3>{doctorInfo.full_name}</h3>
              <p><strong>Department:</strong> {doctorInfo.department}</p>
              <p><strong>Description:</strong> {doctorInfo.about || 'No description available'}</p>
            </div>
          </div>
        )}

        {error && <p className="error-message">{error}</p>}

        <form onSubmit={handleSubmit} className="appointment-form">
          <div className="appointment-date-time">
            <div className="date-selector">
              {availableSlots.map((slot, index) => (
                <button
                  key={index}
                  type="button"
                  className={`date-button ${appointmentData.appointmentDate === slot.date ? 'active' : ''}`}
                  onClick={() =>
                    setAppointmentData({
                      ...appointmentData,
                      appointmentDate: slot.date,
                      appointmentTime: '',
                    })
                  }
                >
                  <div className="day">{new Date(slot.date).toLocaleDateString('en-US', { weekday: 'short' }).toUpperCase()}</div>
                  <div className="date">{new Date(slot.date).getDate()}</div>
                </button>
              ))}
            </div>
          </div>

          <div className="time-selector">
            {availableSlots
              .find(slot => slot.date === appointmentData.appointmentDate)
              ?.daySlots.map((timeSlot, index) => {
                const timeStr = timeSlot.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                return (
                  <button
                    key={index}
                    type="button"
                    className={`time-button ${appointmentData.appointmentTime === timeSlot.toLocaleTimeString() ? 'active' : ''}`}
                    onClick={() =>
                      setAppointmentData({
                        ...appointmentData,
                        appointmentTime: timeSlot.toLocaleTimeString(),
                      })
                    }
                  >
                    {timeStr}
                  </button>
                );
              })}
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              name="description"
              value={appointmentData.description}
              onChange={handleChange}
              placeholder="Describe your symptoms or reason for appointment"
              required
            />
          </div>

          <button type="submit" disabled={loading} className="submit-button">
            {loading ? 'Creating Appointment...' : 'Create Appointment'}
          </button>
        </form>
      </div>
      <Footer/>
    </div>
  );
};

export default AppointmentPage;
