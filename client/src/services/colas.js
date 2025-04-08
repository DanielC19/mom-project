import config from "../config/index"

const create= async (queueId)=>{
    const {data} = await config.API.post("/queue",{
        queue_id: queueId
    }).catch(err=>{
        return { data: {
            success:false,
            message: err.message
            }
        }
    });
    return data;
}

const getQueues = async ()=>{
    const {data} = await config.API.get("/queue")
    .catch(err=>{
        return { data: {
            success:false,
            message: err.message
            }
        }
    });
    return data;
}

const getMessages = async (queueId)=>{
    const {data} = await config.API(`/queue/${queueId}`)
    .catch(err=>{
        return { data: {
            success:false,
            message: err.message
            }
        }
    });
    return data;
}

const sendMessage = async (quueId, message, user)=>{
    const {data} =  await config.API.put(`/queue/${quueId}`, { content: message, sender: user })
    .catch(err=>{
        return { data: {
            success:false,
            message: err.message
            }
        }
    });
    return data;
}

const methots ={
    create,
    getMessages,
    sendMessage,
    getQueues
};

export default methots;