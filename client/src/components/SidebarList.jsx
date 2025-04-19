
import { Plus } from "lucide-react";
import "../styles/main.css";

export default function SidebarList({queues, openOver, selectChat, topics, selectedToShow, setselectedToShow, setMessages,selectedChat, user}) {
  
  return (
    <div className="conatct-list">
    <h4 
      style={{marginLeft: "1.5em"}}
      onClick={()=>setselectedToShow("colas")} 
      className={selectedToShow==="colas"?"selected active": "selected"
      }>Colas</h4>
    <h4 
      onClick={()=>setselectedToShow("topicos")} 
      className={selectedToShow==="topicos"?"selected active": "selected"}
      >Topicos</h4>
      <Plus size={15} className="more-icon" onClick={openOver} />
    <hr/>
    <div className="scroll-area">
      {(selectedToShow==="colas"&& queues!==null)? queues.map((queue)=>(
        <div key={queue.topicId} className="queue-item" onClick={()=>{
          if(!(queue===selectedChat.id && selectedChat.type==="c")) setMessages([]);
          selectChat({
            type: "c",
            id: queue.topicId
          })
        }}>
          <p className="queue-name">{queue}</p>
        </div>
      )
      ):topics.map((topic)=>(
        <div key={topic.topicId} className="queue-item"onClick={()=>{
          if(!(topic.topicId===selectedChat.id && selectedChat.type==="t")) setMessages([]);
            selectChat({
            type: "t",
            id: topic.topicId
          })
                  }}>
          <p className="queue-name">{topic}</p>
        </div>
      )
      )}
    </div>
  </div>
  );
}
