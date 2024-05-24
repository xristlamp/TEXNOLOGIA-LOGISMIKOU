// src/App.js
import React, { useState, useEffect } from 'react';
import { Route, Routes, Link, useNavigate } from 'react-router-dom';
import './App.css';
import Login from './Login';
import Register from './Register';
import UserHome from './components/UserHome';
import AddPet from './components/AddPet';
import Cookies from 'js-cookie';

function App() {
  const [auth, setAuth] = useState({ isAuthenticated: false, role: '' });
  const [userId, setUserId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const cookie = Cookies.get('user');
    if (cookie) {
      const user = JSON.parse(cookie);
      setAuth({ isAuthenticated: true, role: user.role });
      setUserId(user.userId);
    }
  }, []);

  const handleLoginSuccess = (role, id) => {
    setAuth({ isAuthenticated: true, role });
    setUserId(id);
    Cookies.set('user', JSON.stringify({ userId: id, role }), { expires: 7 });
    if (role === 'user') {
      navigate('/user-home');
    }
  };

  const handleLogout = () => {
    setAuth({ isAuthenticated: false, role: '' });
    setUserId(null);
    Cookies.remove('user');
    navigate('/');
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
          {auth.isAuthenticated && auth.role === 'user' && (
            <>
              <li>
                <Link to="/add-pet">Add Pet</Link>
              </li>
              <li>
                <button onClick={handleLogout}>Logout</button>
              </li>
            </>
          )}
        </ul>
      </nav>
      <Routes>
        <Route path="/login" element={<Login onLoginSuccess={handleLoginSuccess} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<h1>Welcome to the App</h1>} />
        <Route path="/user-home" element={auth.isAuthenticated && auth.role === 'user' ? <UserHome userId={userId} /> : <Login onLoginSuccess={handleLoginSuccess} />} />
        <Route path="/add-pet" element={auth.isAuthenticated && auth.role === 'user' ? <AddPet userId={userId} /> : <Login onLoginSuccess={handleLoginSuccess} />} />
      </Routes>
    </div>
  );
}

export default App;
