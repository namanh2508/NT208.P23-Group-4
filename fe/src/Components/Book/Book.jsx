import React from 'react'
import "./Book.css"
import Electrocardiogram from "../../assets/Electrocardiogram.png"
const Book = () => {
  return (
    <div className='book'>
      <img id='img' src={Electrocardiogram} alt="" />
      <div className='book-text'>
        <h2>Having A Health Problem? Don't Make Delay On Your Life</h2>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Consectetur ut, quidem architecto quisquam enim vitae aperiam voluptatibus velit asperiores provident esse sequi, sed veritatis tempore laborum, ad quam placeat ex.</p>
        <button id='btn'>Book an Appointment</button>
      </div>
    </div>
  )
}
export default Book
