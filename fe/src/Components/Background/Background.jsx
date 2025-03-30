import './Background.css'
import { useEffect, useState } from "react";
import video1 from "../../assets/video1.mp4"
import image1 from "../../assets/image1.jpg"
import image2 from '../../assets/image2.jpg'
import image3 from '../../assets/image3.jpg'

const Background = ({ playStatus, heroCount }) => {
  const [currentImage, setCurrentImage] = useState(image1);
  const [fade, setFade] = useState(false);

  useEffect(() => {
    setFade(true);

    setTimeout(() => {
      setCurrentImage(heroCount === 0 ? image1 : heroCount === 1 ? image2 : image3);
    }, 500); 

    setTimeout(() => {
      setFade(false);
    }, 500);
  }, [heroCount]);

  if (playStatus) {
    return (
      <video className="background fade-in" autoPlay loop muted>
        <source src={video1} type="video/mp4" />
      </video>
    );
  }

  return (
    <img
      src={currentImage}
      className={`background fade-in ${fade ? "fade-out" : "fade-in-blur"}`}
      alt=""
    />
  );
};

export default Background
