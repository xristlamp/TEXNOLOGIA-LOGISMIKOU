import React, { useState } from 'react';
import { Route, Routes, Link, useNavigate } from 'react-router-dom';
import './App.css';
import Login from './Login';
import Register from './Register';
import UserHome from './UserHome';
import VetHome from './VetHome';
import GroomerHome from './GroomerHome';
import TrainerHome from './TrainerHome';
import PetSitterHome from './PetSitterHome';

function App() {
  const [auth, setAuth] = useState({ isAuthenticated: false, role: '' });
  const navigate = useNavigate();

  const handleLoginSuccess = (role) => {
    setAuth({ isAuthenticated: true, role });
    switch (role) {
      case 'user':
        navigate('/user-home');
        break;
      case 'vet':
        navigate('/vet-home');
        break;
      case 'groomer':
        navigate('/groomer-home');
        break;
      case 'trainer':
        navigate('/trainer-home');
        break;
      case 'pet-sitter':
        navigate('/pet-sitter-home');
        break;
      default:
        navigate('/');
    }
  };

  return (
    <div className="App">
      <nav>
        <ul>
          <li>
            <Link to="/login">Login</Link>
          </li>
          <li>
            <Link to="/register">Register</Link>
          </li>
        </ul>
      </nav>
      <Routes>
        <Route path="/login" element={<Login onLoginSuccess={handleLoginSuccess} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<h1>Welcom to the App</h1>} />
        <Route path="/user-home" element={auth.isAuthenticated && auth.role === 'user' ? <UserHome /> : <Login onLoginSuccess={handleLoginSuccess} />} />
        <Route path="/vet-home" element={auth.isAuthenticated && auth.role === 'vet' ? <VetHome /> : <Login onLoginSuccess={handleLoginSuccess} />} />
        <Route path="/groomer-home" element={auth.isAuthenticated && auth.role === 'groomer' ? <GroomerHome /> : <Login onLoginSuccess={handleLoginSuccess} />} />
        <Route path="/trainer-home" element={auth.isAuthenticated && auth.role === 'trainer' ? <TrainerHome /> : <Login onLoginSuccess={handleLoginSuccess} />} />
        <Route path="/pet-sitter-home" element={auth.isAuthenticated && auth.role === 'pet-sitter' ? <PetSitterHome /> : <Login onLoginSuccess={handleLoginSuccess} />} />
      </Routes>
    </div>
  );
}

export default App;
