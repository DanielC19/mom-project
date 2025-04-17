import config from "../config/index"

const create = async (token, queueId) => {
    const {data} = await config.API.post("/queue",
        { queue_id: queueId },
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

const getQueues = async (token) => {
    const {data} = await config.API.get("/queue",
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

const getMessages = async (token, queueId) => {
    const {data} = await config.API.get(`/queue/${queueId}`,
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

const sendMessage = async (token, queueId, message) => {
    const {data} = await config.API.put(`/queue/${queueId}`,
        { content: message },
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
    getQueues
};

export default methots;