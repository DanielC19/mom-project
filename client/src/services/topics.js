import config from "../config/index"

const create = async (token, topic_id) => {
    const {data} = await config.API.post("/topic",
        { topic_id: topic_id },
        { headers: { Authorization: `Bearer ${token}` } }
    ).catch(err => {
        console.log(err);
        return { data: {
            success: false,
            message: err.message
        } }
    });
    return data;
}

const getTopics = async (token) => {
    const {data} = await config.API.get("/topics",
        { headers: { Authorization: `Bearer ${token}` } }
    ).catch(err => {
        return { data: {
            success: false,
            message: err.message
        } }
    });
    return data;
}

const getMessages = async (token, topic_id) => {
    const {data} = await config.API.get(`/topic/${topic_id}/pull`,
        { headers: { Authorization: `Bearer ${token}` } }
    ).catch(err => {
        return { data: {
            success: false,
            message: err.message
        } }
    });
    return data;
}

const sendMessage = async (token, quueId, message) => {
    const {data} = await config.API.post(`/topic/${quueId}/publish`,
        { content: message },
        { headers: { Authorization: `Bearer ${token}` } }
    ).catch(err => {
        return { data: {
            success: false,
            message: err.message
        } }
    });
    return data;
}

const suscribe = async (token, topicId) => {
    const {data} = await config.API.post(`/topic/${topicId}/subscribe`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
    ).catch(err => {
        return { data: {
            success: false,
            message: err.message
        } }
    });
    return data;
}


const Delete = async (token, topicId) => {
    const {data} = await config.API.delete(`/topic/${topicId}`,
        { headers: { Authorization: `Bearer ${token}` } }
    ).catch(err => {
        return { data: {
            success: false,
            message: err.message
            }
        }
    });
    return data;
}

const methots = {
    create,
    getMessages,
    sendMessage,
    getTopics,
    suscribe,
    Delete
};

export default methots;