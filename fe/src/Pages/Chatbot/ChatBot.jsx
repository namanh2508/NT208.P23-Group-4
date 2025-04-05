import { useEffect, useRef, useState } from "react";
import ChatbotIcon from "./ChatbotIcon";
import ChatForm from "./ChatForm";
import './index.css';
import ChatMessage from "./ChatMessage";
import comment from "../../assets/comment.svg";
import xmark from "../../assets/xmark.svg";
import chevron from "../../assets/chevron-down.svg";
import { Info } from "./info";
const ChatBot = () => {
  const chatBodyRef=useRef();
  const [chatHistory,setChatHistory]=useState([{
    hideInChat:true,
    role:"model",
    text:Info
  }]);
  
  const generateBotRespone=async(history)=>{
    const updateHistory=(text)=>{
      setChatHistory(prev => [...prev.filter(msg=>msg.text!=="Doctor is Thinking..."),{role:"model",text}])
    }

    history=history.map(({role,text})=>({role,parts:[{text}]}));
    const requestOptions={
      method:"POST",
      headers:{"Content-Type": "application/json"},
      body:JSON.stringify({contents:history})
    }
    try{
      const response=await fetch(import.meta.env.VITE_API_URL_CHATBOT,requestOptions);
      const data = await response.json();
      if(!response.ok) throw new Error(data.error.message||"Something went wrong!");
      const apiResponseText = data.candidates[0].content.parts[0].text.replace(/\*\*(.*?)\*\*/g,"$1").trim();
      updateHistory(apiResponseText);
    } catch(error){
      console.log(error)
    }
  }
  useEffect(()=>{
    chatBodyRef.current.scrollTo({top:chatBodyRef.current.scrollHeight,behavior:"smooth"});
  },[chatHistory]);
  const [showChatbot,setShowChatbot]=useState(false);
  return (
    <div className={`container ${showChatbot ? "show-chatbot" : ""}`}>
      <button id="chatbot-toggler" onClick={() => setShowChatbot(!showChatbot)}>
        <img src={comment} alt="showchatbot"></img>
        <img src={xmark} alt="closechatbot"></img>
      </button>
      <div className="chatbot-popup">
        {/* Header */}
        <div className="chat-header">
          <div className="header-info">
            <ChatbotIcon/>
            <h2 className="logotext">Chatbot</h2>
          </div>
          <button id="close-btn" onClick={() => setShowChatbot(!showChatbot)}>
            <img  src={chevron} alt="closeChatbot"></img>
          </button>
        </div>
        {/* body */}
        <div ref={chatBodyRef} className="chat-body">
          <div className="message bot-message">
            <ChatbotIcon/>
            <p className="message-text">Bạn đang có vấn đề gì với sức khỏe của mình không? Hãy chia sẽ cho tôi biết nhé</p>
          </div>

          {chatHistory.map((chat,index)=>(
            <ChatMessage key={index} chat={chat}/>
          ))}
        </div>


        <div className="chat-footer">
          <ChatForm chatHistory={chatHistory} setChatHistory={setChatHistory} generateBotRespone={generateBotRespone}/>
        </div>
      </div>
    </div>
  );
};

export default ChatBot;