import config from "../config/index"

const create= async (topic_id)=>{
    const {data} = await config.API.post("/topic",{
        topic_id: topic_id
    }).catch(err=>{
        console.log(err);
        return { data: {
                success: false,
                message: err.message
                }
            }
    });

    return data;
}

const getTopics = async ()=>{
    const {data} = await config.API.get("/topics")
    .catch(err=>{
        return { data: {
            success:false,
            message: err.message
            }
        }
    });
    
    return data;
}


const getMessages = async (topic_id, user)=>{
    const {data} = await config.API(`/topic/${topic_id}/pull/${user}`)
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
    const {data} = await config.API.post(`/topic/${quueId}/publish`, { content: message, sender: user })
    .catch(err=>{
        return { data: {
            success:false,
            message: err.message
            }
        }
    });
    return data;
}

const suscribe = async (topicId, user)=>{
    const {data} = await config.API.post(`/topic/${topicId}/subscribe/${user}`)
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
    getTopics,
    suscribe
};

export default methots;