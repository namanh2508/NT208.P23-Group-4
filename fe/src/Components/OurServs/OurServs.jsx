import './OurServs.css'
import ai from "../../assets/ai.svg"
import calender from "../../assets/calender.svg"
import magnifying from "../../assets/magnifying.svg"
import stethoscope from "../../assets/stethoscope.svg"
import { useEffect } from 'react'
const OurServs = () => {
  useEffect(() => {
    const boxes = document.querySelectorAll(".box");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("show");
          }
        });
      },
      { threshold: 0.2 }
    );

    boxes.forEach((box) => observer.observe(box));
    
    return () => boxes.forEach((box) => observer.unobserve(box));
  }, []);
  return (
    <div className='ourservs'>
      <div className="ourservs-text">
        <p>Our Services</p>
      </div>
      <div className="boxes">
        <div className="box">
            <div className="icon-wrapper"><img className='ourservs-icon' src={ai} alt="" /></div>
            <h4>AI Support</h4>
            <p>Lorem ipsum, dolor sit amet consectetur adipisicing.</p>
        </div>
        <div className="box">
            <div className="icon-wrapper"><img className='ourservs-icon' src={calender} alt="" /></div>
            <h4>Book an Appointment</h4>
            <p>Lorem ipsum, dolor sit amet consectetur adipisicing.</p>

        </div>
        <div className="box">
            <div className="icon-wrapper"><img className='ourservs-icon' src={magnifying} alt="" /></div>
            <h4>Drug Information</h4>
            <p>Lorem ipsum, dolor sit amet consectetur adipisicing.</p>

        </div>
        <div className="box">
            <div className="icon-wrapper"><img className='ourservs-icon' src={stethoscope} alt="" /></div>
            <h4>Talk to a Doctor</h4>
            <p>Lorem ipsum, dolor sit amet consectetur adipisicing.</p>
        </div>
      </div>
    </div>
  )
}

export default OurServs
