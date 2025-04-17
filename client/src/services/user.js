import config from "../config/index"

const create = async (userId, userName) => {
    const { data } = await config.API.post("/user", {
        username: userId,
        password: userName
    }).catch(err => {
        return { data: { success: false, message: err.message } }
    });
    console.log(data);
    return data;
}

const  logIn= async (username, password) => {
    const { data } = await config.API.post("/login", {
        username: username,
        password: password
    }).catch(err => {
        return { data: { success: false, message: err.message } }
    });
    return data;
}

const methots = {
    create,
    logIn
}

export default methots;