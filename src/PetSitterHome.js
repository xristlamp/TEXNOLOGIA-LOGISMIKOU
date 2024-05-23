import React from 'react';
import { Link } from 'react-router-dom';

const VetHome = () => {
  return (
    <div>
      <h2>Vet Home</h2>
      <button><Link to="/profile">My Profile</Link></button>
      <button><Link to="/reservations">My Reservations</Link></button>
      <button><Link to="/upload-work">Upload Work</Link></button>
    </div>
  );
};

export default VetHome;
