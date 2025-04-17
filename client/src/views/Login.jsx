
import userAPI from "../services/user";
// import '../styles/tailwind.css';
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { LoginForm } from "../components/LoginForm";
import { loginFields } from "../constants/formFields";

let fieldsState = {};
loginFields.forEach(field => fieldsState[field.name] = '');

function Login({ setUser }) {
  const [loginState, setLoginState] = useState(fieldsState);
  const [errorState, setErrorState] = useState();
  const navigate = useNavigate();

  const handleChange = event => {
    setLoginState({...loginState, [event.target.id]: event.target.value})
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    userAPI.logIn(loginState.name, loginState.password)
      .then(res => {
        if (res.success) {
          navigate(`/chat?user=${res.token}`);
        } else {
          setErrorState(res.message);
        }
      })
      .catch(err => {
        setErrorState(err.message);
      });
  }

  return(
    <LoginForm
      state={loginState}
      handleChange={handleChange}
      handleSubmit={handleSubmit}
      title="Inicia sesión"
      subtitle="¿Aún no tienes cuenta?"
      link="Regístrate"
      linkUrl="/register" 
      fields={loginFields}
      buttonLabel="Iniciar sesión"
      error={errorState}
    />
  );
}

export default Login;
