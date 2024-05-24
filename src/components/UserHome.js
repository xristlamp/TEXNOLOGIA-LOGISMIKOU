// src/components/UserHome.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserHome = ({ userId }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/users/${userId}`);
        setUser(response.data);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };
    fetchUser();
  }, [userId]);

  if (!user) return <div>Loading...</div>;

  return (
    <div>
      <h1>{user.username}'s Profile</h1>
      <h2>Pets</h2>
      <ul>
        {user.pets.map((pet, index) => (
          <li key={index}>{pet.name} ({pet.species})</li>
        ))}
      </ul>
    </div>
  );
};

export default UserHome;
