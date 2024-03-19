import logo from './logo.svg';
import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import AuthCallbackPage from './pages/Callback';
import Home from './pages/Home';
import Login from './pages/Login';

function App() {
  return (
   <BrowserRouter>
    <Routes>
      <Route path="/callback" element={<AuthCallbackPage />} />
      <Route path="/home" element={<Home/>} />
      <Route path="/" index element={<Login />} />
    </Routes>
   </BrowserRouter>
  );
}

export default App;
