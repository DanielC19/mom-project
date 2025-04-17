import ChatView from "./views/chatView";
import {BrowserRouter as Router, Routes, Route} from "react-router-dom"
import './styles/App.css';
import Register from "./views/Register";
import Login from "./views/Login";

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<ChatView/>}/>
        <Route path='register' element={
            <Register />
          } />
          <Route path='login' element={
            <Login />
          } />
      </Routes>
    </Router>
  );
}

export default App;
