import './About.css'
import chevron from "../../assets/chevron.svg"
import image4 from "../../assets/image4.jpg"
const About = () => {
  return (
    <div className='about'>
        <div className="about-text">
            <h3>About</h3>
            <h2>HOSPITAL MANAGEMENT SYSTEM</h2>
            <p>A Hospital Management System (HMS) is a comprehensive software solution designed to streamline hospital operations, including patient records, appointment scheduling, billing, inventory management, and staff coordination. It enhances efficiency, reduces paperwork, and ensures better patient care by integrating various hospital departments into a single, centralized system.
</p>
            <div className="about-explore">
                <p>Read More</p>
                <img className='about-icon' src={chevron} alt=""/>
            </div>
        </div>
        <div className='about-pict'>
            <div className='about-btns'>
                <div className='about-btn'>
                    <p>Appointment</p>
                    <img className='about-icon1' src={chevron} alt="" />
                </div>
                <div className='about-btn'>
                    <p>Find Doctor</p>
                    <img className='about-icon1' src={chevron} alt="" />
                </div>
                <div className='about-btn'>
                    <p>Emergency Contact</p>
                    <img className='about-icon1' src={chevron} alt="" />
                </div>
            </div>
            <img src={image4} alt=''/>
        </div>
    </div>
  )
}

export default About
