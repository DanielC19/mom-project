import { useState, useEffect, useRef } from "react";
import "../styles/main.css";
import queueAPI from "../services/colas"
import topicAPI from "../services/topics"
import { Send } from "lucide-react";

function ChatContainer({ selectedChat, selected, messages, setMessages, user, setMode, mode }) {
  const [message, setMessage] = useState("");
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }); 
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim()) return; 

    const newMessage = {
      text: message,
      sender: user,
      timestamp: new Date().toISOString(), 
    };

    try {
      if (selected === "topicos") {
        await topicAPI.sendMessage(user, selectedChat.id, message);
      } else {
        await queueAPI.sendMessage(user, selectedChat.id, message);
      }
      setMessages((prevMessages) => [...prevMessages, newMessage]);
      setMessage("");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2 className="chat-title">{selectedChat.id !== null ? selectedChat.id : "Chat"}</h2>
        <select onChange={(e)=>{setMode(e.target.value)}} className="rol_select" >
          <option value="r">Recibir</option>
          <option  value="e">Enviar</option>
        </select>
      </div>
      <div class="messages-container">
        <ul className="chat-messages">
          {messages.map((msg, index) => (
            <li
              key={index}
              className={`message ${
                msg.sender === user ? "sent" : "received"
              }`}
            >
              <div className="message-content">{msg.text}</div>
              <div className="message-timestamp">
              {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }
              </div>
            </li>
          ))}
          <div ref={messagesEndRef} />
        </ul>
      </div>
      {(selectedChat !== null && mode==="e") && (
        <form className="chat-input-container" onSubmit={sendMessage}>
          <input
            type="text"
            placeholder="Escribe un mensaje..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="chat-input"
          />
          <button type="submit" className="send-button">
            < Send size={20} />
          </button>
        </form>
      )}
    </div>
  );
}

export default ChatContainer;
