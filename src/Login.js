import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [userId, setUserId] = useState(null);
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState(1);
  const [error, setError] = useState('');
  const [role, setRole] = useState('');
  const navigate = useNavigate();

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await axios.post('http://localhost:5000/api/login', { username, password });
      setUserId(response.data.userId);
      setRole(response.data.role); // Assuming the response includes the role
      setStep(2);
    } catch (error) {
      if (error.response && error.response.status === 401) {
        setError('Invalid username or password');
      } else {
        setError('An error occurred. Please try again.');
      }
    }
  };

  const handleOtpSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await axios.post('http://localhost:5000/api/verify-otp', { userId, otp });
      onLoginSuccess(role); // Pass the role to the onLoginSuccess callback
    } catch (error) {
      if (error.response && error.response.status === 401) {
        setError('Invalid OTP');
      } else {
        setError('An error occurred. Please try again.');
      }
    }
  };

  return (
    <div>
      {step === 1 && (
        <form onSubmit={handleLoginSubmit}>
          <h2>Login</h2>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          <div>
            <label>Username</label>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
          </div>
          <div>
            <label>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          <button type="submit">Login</button>
        </form>
      )}
      {step === 2 && (
        <form onSubmit={handleOtpSubmit}>
          <h2>Enter OTP</h2>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          <div>
            <label>OsTP</label>
            <input type="text" value={otp} onChange={(e) => setOtp(e.target.value)} />
          </div>
          <button type="submit">Verify OTP</button>
        </form>
      )}
    </div>
  );
};

export default Login;
