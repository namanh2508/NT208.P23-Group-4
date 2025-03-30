import './Doctor.css'
import doctor1 from "../../assets/doctor1.png"
import doctor2 from "../../assets/doctor2.png"
import doctor3 from "../../assets/doctor3.png"
import doctor4 from "../../assets/doctor4.png"
const Doctor = () => {
  return (
    <div className='doctor'>
      <h2>Our Doctor</h2>
      <div className='contains'>
          <div className='contain'>
            <div className='img'><img src={doctor1} alt="" /></div>
            <h4>Dr.John Doe</h4>
            <p>Cardiologist</p>
            <button>Get advice now</button>
          </div>
          <div className='contain'>
            <div className='img'><img src={doctor2} alt="" /></div>
            <h4>Dr.Luna Brawn</h4>
            <p>Neurologist</p>
            <button>Get advice now</button>
          </div>
          <div className='contain'>
            <div className='img'><img src={doctor3} alt="" /></div>
            <h4>Dr.Harry Potter</h4>
            <p>Dentist</p>
            <button>Get advice now</button>
          </div>
          <div className='contain'>
            <div className='img'><img src={doctor4} alt="" /></div>
            <h4>Dr.Shin Nosuke</h4>
            <p>clown</p>
            <button>Get advice now</button>
          </div>
      </div>
    </div>
  )
}

export default Doctor
