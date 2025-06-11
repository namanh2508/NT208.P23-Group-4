import { useEffect, useState } from "react";
import { getPatientProfile } from '../../Components/api'; 
import Footer from "../../Components/Footer/Footer";
import Navbar from "../../Components/Navbar/Navbar";
import './Profile.css';
const ProfilePage = ({ isAuthenticated }) => {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
        const data = await getPatientProfile();
        setProfile(data);
    };

    fetchProfile();
  }, []);

  if (!profile) return <p>Loading...</p>;

  return (
    <div>
        <div className='navbar1'>
        <Navbar isAuthenticated={isAuthenticated} />
        </div>
        <div className="profile-container">
        <h2>Personal Information</h2>
        <img src={profile.picture} alt="Profile" />
        <div className="profile-info">
            <p><strong>Name:</strong> {profile.first_name} {profile.last_name}</p>
            <p><strong>Username:</strong> {profile.username}</p>
            <p><strong>Email:</strong> {profile.email}</p>
            <p><strong>Phone:</strong> {profile.phone}</p>
            <p><strong>Gender:</strong> {profile.gender}</p>
            <p><strong>Birthday:</strong> {profile.birthday}</p>
            <p><strong>Height:</strong> {profile.height} cm</p>
            <p><strong>Weight:</strong> {profile.weight} kg</p>
            <p><strong>Family Phone:</strong> {profile.family_phone}</p>
            <p><strong>Description:</strong> {profile.description}</p>
        </div>
        </div>
        <Footer />
    </div>
    );
};

export default ProfilePage;
