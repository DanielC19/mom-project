import { Plus, Trash2 } from "lucide-react";
import "../styles/main.css";

import queueAPI from "../services/colas";
import topicAPI from "../services/topics";

export default function SidebarList({queues, openOver, selectChat, topics, selectedToShow, setselectedToShow, setMessages,selectedChat, username, user}) {
  
  const handleDelete = async (id, type) => {
    if(type==="c"){
      const res = await queueAPI.Delete(user, id);
      if(res.success){
        alert("Cola eliminada");
      }else{
        alert("Error al eliminar la cola: "+res.message);
      }
    }else{
      const res = await topicAPI.Delete(user, id);
      if(res.success){
        alert("Topico eliminada");
      }else{
        alert("Error al eliminar el topico: "+res.message);
      }
    }
  };

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
        <div key={queue.topicId} className="queue-item" style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }} onClick={()=>{
          if(!(queue.queue_id===selectedChat.id && selectedChat.type==="c")) setMessages([]);
          selectChat({
            type: "c",
            id: queue.queue_id
          })
        }}>
          <p className="queue-name">{queue.queue_id}</p>
          
            {
            username===queue.autor ? (<>
            <button 
            style={{ background: "red", border: "none", padding: "5px", borderRadius: "50%", cursor: "pointer" }}
            onClick={(e) => { e.stopPropagation(); handleDelete(queue.queue_id, "c"); }}
            >
              <Trash2 size={15} color="white" style={{cursor: "pointer"}} />
            </button>
            </>):(<></>)
          }
          
        </div>
      )
      ):topics.map((topic)=>(
        <div key={topic.topicId} className="queue-item" style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }} onClick={()=>{
          if(!(topic.topic_id===selectedChat.id && selectedChat.type==="t")) setMessages([]);
            selectChat({
            type: "t",
            id: topic.topic_id
          })
                  }}>
          <p className="queue-name">{topic.topic_id}</p>
          {
            username===topic.autor ? (<>
            <button 
            style={{ background: "red", border: "none", padding: "5px", borderRadius: "50%", cursor: "pointer" }}
            onClick={(e) => { e.stopPropagation(); handleDelete(topic.topic_id, "t"); }}
            >
              <Trash2 size={15} color="white" style={{cursor: "pointer"}} />
            </button>
            </>):(<></>)
          }
        </div>
      )
      )}
    </div>
  </div>
  );
}
