import axios from 'axios';
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
    axios.post('/api/register', registerState).then(
      // On success
      ({response}) => {
        //
      },
      // On error
      ({response}) => {
        //
      }
    );
  }

  return(
    <LoginForm
      state={registerState}
      handleChange={handleChange}
      handleSubmit={handleSubmit}
      title="Crea una cuenta"
      subtitle="¿Ya tienes una?"
      link="Inicia sesión"
      linkUrl="/login"
      fields={registerFields}
      buttonLabel="Regístrate"
      error={errorState}
    />
  );
}

export default Register;
