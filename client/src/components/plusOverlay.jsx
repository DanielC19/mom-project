import { useState } from "react";
import queueAPI from "../services/colas";
import topicAPI from "../services/topics";
import "../styles/overlay.css";

function PlusOverlay({ setCreatedForMe, isOpen, onClose }) {
  const [selected, setSelected] = useState("Crear");
  const [select, setSelect] = useState("Colas");
  const [idToCreate, setIdToCreate] = useState("");
  const listaOpciones = ["Colas", "Topicos"];

  const handleSubmit = async (e)=>{
    e.preventDefault();
    if(select==="Colas"){
      const res =await queueAPI.create(idToCreate);
      onClose();
      if(!res.error) setCreatedForMe(prev=>[...prev, idToCreate]);
      alert(res.message);
    }else{
      const res = await topicAPI.create(idToCreate);
      if(!res.error) setCreatedForMe(prev=>[...prev, idToCreate]);
      alert(res.message);
      onClose();
    }
  }

  if (!isOpen) return null;

  return (
    <div className="overlay">
      <div className="modal">
        {/* Encabezado con botones para cambiar entre Colas y Tópicos */}
        <div className="modal-header">
          <button
            className={`tab-button ${selected === "Crear" ? "active" : ""}`}
            onClick={() => setSelected("Crear")}
          >
            Crear
          </button>
          <button
            className={`tab-button ${selected === "Suscribir" ? "active" : ""}`}
            onClick={() => setSelected("Suscribir")}
          >
            Suscribir
          </button>
        </div>

        {/* Contenido dinámico basado en la opción seleccionada */}
        <div className="modal-content">
          {selected === "Crear" ? <>
          <form onSubmit={handleSubmit}>
            <div className="form-container">
              <select className="form-select" name="create" id="" value={select} onChange={(e)=>setSelect(e.target.value)}>
                { listaOpciones.map((e)=>(
                  <>
                    <option value={e}>{e}</option>
                  </>
                ))}
              </select>
              <input 
              className="form-input" 
              type="text" 
              name="id" 
              value={idToCreate}
              placeholder="Ingrese un nombre..."
              onChange={(e)=>setIdToCreate(e.target.value)}
              />
              <button className="form-button">Send</button>
            </div>
          </form>
          </> : <p>Opciones de Tópicos...</p>}
        </div>

        <div className="modal-actions">
          <button className="modal-button cancel" onClick={onClose}>
            Cancelar
          </button>
        </div>
      </div>
    </div>
  );
}

export default PlusOverlay;
