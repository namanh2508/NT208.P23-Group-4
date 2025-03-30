import './Hero.css'
import arrow_btn from "../../assets/arrow.svg"
import pause_icon from "../../assets/pause.svg"
import play_icon from "../../assets/play.svg"
const Hero = ({heroData,heroCount,setHeroCount,playStatus,setPlayStatus,ourServsRef}) => {
  const scrollToServices = () => {
    if (ourServsRef.current) {
      ourServsRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };
  return (
    <div className='hero'>
      <div className="hero-text">
        <p>{heroData[heroCount].text1}</p>
        <p>{heroData[heroCount].text2}</p>
      </div>
      <div className="hero-explore" onClick={scrollToServices}>
        <p>See our service</p>
        <div className="wrapper">
          <img className='hero-icon' src={arrow_btn} alt=""/>
        </div>
      </div>
      <div className='hero-dot-play'>
        <ul className={playStatus?"hero-dots-hidden":"hero-dots"}>
          <li onClick={()=>setHeroCount(0)} className={heroCount===0?"hero-dot bluee":"hero-dot"}></li>
          <li onClick={()=>setHeroCount(1)} className={heroCount===1?"hero-dot bluee":"hero-dot"}></li>
          <li onClick={()=>setHeroCount(2)} className={heroCount===2?"hero-dot bluee":"hero-dot"}></li>
        </ul>
        <div className='hero-play'>
          <img className='heroicon' onClick={()=>setPlayStatus(!playStatus)} src={playStatus?pause_icon:play_icon} alt="" />
        </div>
      </div>
    </div>
  )
}

export default Hero
