import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:5000",
    withCredentials: false,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });

const config = {
    API: api
  }

export default config