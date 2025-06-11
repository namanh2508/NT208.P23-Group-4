import { useEffect, useState,useRef } from "react";
import Background from "../Components/Background/Background";
import Navbar from "../Components/Navbar/Navbar";
import Hero from "../Components/Hero/Hero";
import About from "../Components/About/About";
import OurServs from "../Components/OurServs/OurServs";
import Book from "../Components/Book/Book";
import Doctor from "../Components/Doctor/Doctor";
import Footer from "../Components/Footer/Footer";
import ChatBot from "./Chatbot/ChatBot";
const HomePage = ({ isAuthenticated }) => {
  let heroData=[
    {text1:"Take Care",text2:"Healthy Health"},
    {text1:"Stay Active",text2:"Sleep Deep"},
    {text1:"Eat Well",text2:"Stay Hydrated"},
  ]
  const [heroCount,setHeroCount]=useState(2);
  const [playStatus,setPlayStatus]=useState(true);
  const ourServsRef = useRef(null);
  useEffect(()=>{
    setInterval(()=>{
      setHeroCount((count)=>{return count===2?0:count+1})
    },3000);
  },[])

  return (
    <div>
      <Navbar isAuthenticated={isAuthenticated}/>
      <Background playStatus={playStatus} heroCount={heroCount}/>
      <Hero 
        heroData={heroData}
        heroCount={heroCount}
        setHeroCount={setHeroCount}
        playStatus={playStatus}
        setPlayStatus={setPlayStatus}
        ourServsRef={ourServsRef}
      />
      <About/>
      <div ref={ourServsRef}>
        <OurServs />
      </div>
      <Book/>
      <Doctor isAuthenticated={isAuthenticated}/>
      <Footer/>
      <ChatBot/>
    </div>
  )
}

export default HomePage
