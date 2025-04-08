import ChatView from "./views/chatView";
import {BrowserRouter as Router, Routes, Route} from "react-router-dom"
import './styles/App.css';

function App() {
  return (
   <Router>
      <Routes>
        <Route path='/' element={<ChatView/>}/>
      </Routes>
   </Router>
  );
}

export default App;
