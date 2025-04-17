import userAPI from "../services/user";
// import '../styles/tailwind.css';
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { LoginForm } from "../components/LoginForm";
import { registerFields } from "../constants/formFields";

let fieldsState = {};
registerFields.forEach(field => fieldsState[field.name] = '');

function Register({ setUser }) {
  const [registerState, setRegisterState] = useState(fieldsState);
  const [errorState, setErrorState] = useState();
  const navigate = useNavigate();

  const handleChange = event => {
    setRegisterState({...registerState, [event.target.id]: event.target.value})
  }

  const handleSubmit = event => {
    event.preventDefault();
    userAPI.create(registerState.name, registerState.password)
      .then(response => {
        if (response.success) {
          navigate(`/chat?user=${response.token}`);
        } else {
          setErrorState(response.message);
        }
      })
      .catch(error => {
        setErrorState(error.response.data.message);
      });
  }

  return(
    <LoginForm
      state={registerState}
      handleChange={handleChange}
      handleSubmit={handleSubmit}
      title="Crea una cuenta"
      subtitle="¿Ya tienes una?"
      link="Inicia sesión"
      linkUrl="/"
      fields={registerFields}
      buttonLabel="Regístrate"
      error={errorState}
    />
  );
}

export default Register;
