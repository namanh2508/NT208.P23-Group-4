import './Footer.css'
import youtube from "../../assets/youtube.svg"
import facebook from "../../assets/facebook.svg"
import twitter from "../../assets/twitter.svg"
import location from "../../assets/location.svg"
import mail from "../../assets/mail.svg"
import phone from "../../assets/phone.svg"
const Footer = () => {
  return (
    <div className='footer'>
      <div className="footer-main-content">
        <div className="footer-row">
          <div className="footer-column">
            <h2>HostpiAl</h2>
            <p className="footer-desc">
              Lorem ipsum dolor sit amet consectetur, adipisicing elit.
              Obcaecati, dignissimos.
            </p>
            <div className="footer-social">
              <img src={twitter} alt="" className="footer-icon1"/>
              <img src={facebook} alt="" className="footer-icon1"/>
              <img src={youtube} alt="" className="footer-icon1"/>
            </div>
          </div>
          <div className="footer-column">
            <h3 className="footer-title">Company</h3>
            <ul className="footer-list">
              <li><a href="!#">About us</a></li>
              <li><a href="!#">Features</a></li>
              <li><a href="!#">Our pricing</a></li>
              <li><a href="!#">Latest news</a></li>
            </ul>
          </div>
          <div className="footer-column">
            <h3 className="footer-title">Support</h3>
            <ul className="footer-list">
              <li><a href="!#">Top</a></li>
              <li><a href="!#">Jung</a></li>
              <li><a href="!#">Mid</a></li>
              <li><a href="!#">AD carry</a></li>
            </ul>
          </div>
          <div className="footer-column">
            <h3 className="footer-title">Address</h3>
            <ul className="footer-list">
              <li>
                <a href="!#"><img src={location} alt="" className="footer-icon2"/><strong>Location:</strong> UIT university</a>
              </li>
              <li>
                <a href="!#"><img src={mail} alt="" className="footer-icon2"/><strong>Email:</strong> hahahah@gmail.com</a>
              </li>
              <li>
                <a href="!#"><img src={phone} alt="" className="footer-icon2"/><strong>Phone:</strong> +0000 0000 000</a>
              </li>
            </ul>
          </div>
        </div>
        <div className="footer-copyright">
          <p>
          © Group 4 LẬP TRÌNH ỨNG DỤNG WEB

          </p>
        </div>
      </div>
    </div>
  )
}

export default Footer
