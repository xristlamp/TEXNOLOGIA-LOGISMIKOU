// UserProfile.js
import React from 'react';
import AddPet from './AddPet';

const UserProfile = ({ user }) => {
  return (
    <div>
      <h1>{user.username}'s Profiile</h1>
      <h2>Pets</h2>
      <ul>
        {user.pets.map((pet, index) => (
          <li key={index}>{pet.name} ({pet.species})</li>
        ))}
      </ul>
      <AddPet userId={user.id} />
    </div>
  );
};

export default UserProfile;
