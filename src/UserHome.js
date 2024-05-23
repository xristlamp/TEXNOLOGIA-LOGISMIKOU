import React from 'react';
import { Link } from 'react-router-dom';

const UserHome = () => {
  return (
    <div>
      <h2>User Home</h2>
      <button><Link to="/profile">My Profile</Link></button>
      <button><Link to="/vet">Vet</Link></button>
      <button><Link to="/pet-sitting">Pet Sitting</Link></button>
      <button><Link to="/groomer">Groomer</Link></button>
      <button><Link to="/trainer">Educator</Link></button>
    </div>
  );
};

export default UserHome;

