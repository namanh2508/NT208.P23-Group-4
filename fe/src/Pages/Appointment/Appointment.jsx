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
    type: 'general',
    method: 'offline',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [availableSlots, setAvailableSlots] = useState([]);
  const [customDateTime, setCustomDateTime] = useState(false);
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
                src={doctorInfo.picture ? doctorInfo.picture.replace(/^\/+/, '') : '/default-doctor.png'}
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
                  className={`date-button ${appointmentData.appointmentDate === slot.date && !customDateTime ? 'active' : ''}`}
                  onClick={() => {
                    setCustomDateTime(false);
                    setAppointmentData({
                      ...appointmentData,
                      appointmentDate: slot.date,
                      appointmentTime: '',
                    });
                  }}
                >
                  <div className="day">
                    {new Date(slot.date).toLocaleDateString('en-US', { weekday: 'short' }).toUpperCase()}
                  </div>
                  <div className="date">{new Date(slot.date).getDate()}</div>
                </button>
              ))}

              <button
                type="button"
                className={`date-button ${customDateTime ? 'active' : ''}`}
                onClick={() => {
                  setCustomDateTime(true);
                  setAppointmentData({ appointmentDate: '', appointmentTime: '' });
                }}
              >
                <div className="day">OTHER</div>
                <div className="date">+</div>
              </button>
            </div>
          </div>

          <div className="time-selector">
            {!customDateTime &&
              availableSlots
                .find(slot => slot.date === appointmentData.appointmentDate)
                ?.daySlots.map((timeSlot, index) => {
                  const timeStr = timeSlot.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                  const timeKey = timeSlot.toTimeString().split(' ')[0];
                  return (
                    <button
                      key={index}
                      type="button"
                      className={`time-button ${appointmentData.appointmentTime === timeKey ? 'active' : ''}`}
                      onClick={() =>
                        setAppointmentData({
                          ...appointmentData,
                          appointmentTime: timeKey,
                        })
                      }
                    >
                      {timeStr}
                    </button>
                  );
                })}

            {customDateTime && (
              <div className="custom-date-time">
                <label>
                  Chọn ngày:
                  <input
                    type="date"
                    value={appointmentData.appointmentDate}
                    onChange={(e) =>
                      setAppointmentData({
                        ...appointmentData,
                        appointmentDate: e.target.value,
                        appointmentTime: '',
                      })
                    }
                  />
                </label>

                <label>
                  Chọn giờ:
                  <input
                    type="time"
                    value={appointmentData.appointmentTime}
                    onChange={(e) =>
                      setAppointmentData({
                        ...appointmentData,
                        appointmentTime: e.target.value,
                      })
                    }
                  />
                </label>

                <button
                  type="button"
                  onClick={() => {
                    setCustomDateTime(false);
                    setAppointmentData({ appointmentDate: '', appointmentTime: '' });
                  }}
                  style={{ marginTop: '10px' }}
                >
                  Hủy chọn ngày khác
                </button>
              </div>
            )}
          </div>


          <div className="appoint">
            <div className="app-left">
              <div className="form-group">
                <label htmlFor="method">Appointment Method</label>
                <select
                  name="method"
                  value={appointmentData.method}
                  onChange={handleChange}
                  required
                >
                  <option value="offline">Offline (at hospital)</option>
                  <option value="online">Online (video call)</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="type">Appointment Type</label>
                <select
                  name="type"
                  value={appointmentData.type}
                  onChange={handleChange}
                  required
                >
                  <option value="appointment">Appointment</option>
                  <option value="test">Test</option>
                </select>
              </div>
            </div>
            <div className="app-right">
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
            </div>
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
