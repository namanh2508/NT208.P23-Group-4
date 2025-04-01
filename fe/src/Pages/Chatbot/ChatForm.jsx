import { useRef } from "react";
import chevron from "../../assets/chevron-down.svg";

const ChatForm = ({ chatHistory, setChatHistory, generateBotRespone }) => {
  const inputRef = useRef();

  const handleFormSubmit = (e) => {
    e.preventDefault();
    const userMessage = inputRef.current.value.trim();
    if (!userMessage) return;

    inputRef.current.value = ""; 
    inputRef.current.style.height = "30px";
    setChatHistory((history) =>[...history,{role: "user",text:userMessage}]);
        setTimeout(()=>{
            setChatHistory((history) =>[...history,{role: "model",text:"Doctor is Thinking..."}])
            generateBotRespone([...chatHistory,{role: "user", text: `Using the details provided above, please address this query: ${userMessage}` }]);
        },600);
  };

  return (
    <form action="#" className="chat-form" onSubmit={handleFormSubmit}>
      <textarea
        ref={inputRef}
        placeholder="Message..."
        className="message-input"
        rows="1"
        onInput={(e) => {
          e.target.style.height = "auto";
          e.target.style.height = e.target.scrollHeight + "px"; 
        }}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleFormSubmit(e);
          }
        }}
        required
      />
      <button className="btn">
        <img src={chevron} alt="send" id="send-icon" />
      </button>
    </form>
  );
};

export default ChatForm;
