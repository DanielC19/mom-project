import ChatContainer from "../components/chatContaincer";
import SidebarList from "../components/SidebarList";
import { useEffect, useState } from "react";
import queueAPI from "../services/colas"
import topicAPI from "../services/topics"
import { useLocation } from 'react-router-dom';
import PlusOverlay from "../components/plusOverlay";

function ChatView(){
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const user = queryParams.get('user');

  const [showOverlay, setShowOlverlay] = useState(false);
  const [messages, setMessages] = useState([]);
  const [selectedItem, setSelectedItem] = useState({
    type: "",
    id: null
  });
  const [createdForMe, setCreatedForMe] = useState([]);
  const [selectedToShow, setselectedToShow] = useState("colas");
  const [queues, setQueues] = useState([]);
  const [topics, setTopics] = useState([]);
  const [mode, setMode] = useState("r");
  
  useEffect(() => {
    
    const fetchMessages = async () => {
      try {
        if(selectedItem.id!==null && mode==="r"){
          if(selectedToShow==="topicos" ){
            let data = await topicAPI.getMessages(selectedItem.id, user)
            const nuevosMensajes = data.data.map((message) => ({
              text: message.content,
              sender: message.sender,
              timestamp: message.timestamp
            }));

            setMessages((mensajesPrevios) => [...mensajesPrevios, ...nuevosMensajes]);

          }else{
          let data = await queueAPI.getMessages(selectedItem.id);
          if (data.success) setMessages([...messages, {text: data.data.content, sender: "other", timestamp: data.data.timestamp}]); 
          }
        }
      } catch (error) {
        console.error("Error al obtener mensajes:", error);
      }
    };


    const fetchData = async ()=>{
      const Qdata = await queueAPI.getQueues();
      const tData = await topicAPI.getTopics();
      if(tData.success) setTopics(tData.data);
      if(Qdata.success) setQueues(Qdata.data);
    }
    
    const interval = setInterval(fetchData, 3000);
    fetchData();
    if(selectedItem!==null && !createdForMe.includes(selectedItem.id)) fetchMessages();

    return () => clearInterval(interval);
    }, [setQueues, messages,selectedItem, selectedToShow, createdForMe, user, mode]);

    const seleccionarChat = async (nChat)=>{
      if(nChat.type==="t") await topicAPI.suscribe(nChat.id, user)
      setSelectedItem({
        type: nChat.type,
        id: nChat.id
      })
    }

    return(
        <div className="App">
              <PlusOverlay isOpen={showOverlay} onClose={()=>{
                setShowOlverlay(false);
              }
              }
              setCreatedForMe={setCreatedForMe}
              />
              <header className="App-header">
                <SidebarList setMessages={setMessages} selected={selectedToShow} selectedToShow={selectedToShow} setselectedToShow={setselectedToShow} topics={topics} queues={queues} openOver={()=>{
                  setShowOlverlay(true)
                }
              } 
                selectChat={seleccionarChat}
                selectedChat={selectedItem}
                createdForMe={createdForMe}
                />
                <ChatContainer selectedChat={selectedItem} selected={selectedToShow} messages={messages} setMessages={setMessages} user={user} setMode={setMode} mode={mode} />
              </header>
            </div>
    )

}

export default ChatView;