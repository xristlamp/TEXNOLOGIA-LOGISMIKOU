// src/components/AddPet.js
import React, { useState } from 'react';
import axios from 'axios';

const AddPet = ({ userId }) => {
  const [petInfo, setPetInfo] = useState({
    name: '',
    species: '',
    breed: '',
    age: '',
    medicalHistory: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setPetInfo(prevState => ({ ...prevState, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`http://localhost:5000/api/users/${userId}/pets`, petInfo);
      alert(response.data.message);
      // Optionally, clear the form or perform other actions
    } catch (error) {
      alert(error.response.data.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add Pet</h2>
      <div>
        <label>Name:</label>
        <input type="text" name="name" value={petInfo.name} onChange={handleChange} required />
      </div>
      <div>
        <label>Species:</label>
        <input type="text" name="species" value={petInfo.species} onChange={handleChange} required />
      </div>
      <div>
        <label>Breed:</label>
        <input type="text" name="breed" value={petInfo.breed} onChange={handleChange} required />
      </div>
      <div>
        <label>Age:</label>
        <input type="number" name="age" value={petInfo.age} onChange={handleChange} required />
      </div>
      <div>
        <label>Meedical History:</label>
        <textarea name="medicalHistory" value={petInfo.medicalHistory} onChange={handleChange} required />
      </div>
      <button type="submit">Add Pet</button>
    </form>
  );
};

export default AddPet;
