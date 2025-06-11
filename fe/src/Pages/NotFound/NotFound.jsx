import React from 'react'
import Navbar from '../../Components/Navbar/Navbar'
import Footer from '../../Components/Footer/Footer'
import './NotFound.css'
import notfound from '../../assets/notfound.png'
const NotFound = ({ isAuthenticated }) => {
  return (
    <div>
      <div className='navbar1'>
      <Navbar isAuthenticated={isAuthenticated}/>
      </div>
        <div className='not-found'>
            <img src={notfound} alt="" />
        </div>
        <Footer/>
    </div>
  )
}

export default NotFound
