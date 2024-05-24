import React, { useState } from 'react';
import axios from 'axios';

function AddPetForm({ userId }) {
  const [petInfo, setPetInfo] = useState({
    name: '',
    species: '',
    breed: '',
    age: '',
    medicalHistory: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setPetInfo((prevPetInfo) => ({
      ...prevPetInfo,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`/api/users/${userId}/pets`, petInfo);
      alert(response.data.message);
    } catch (error) {
      alert(error.response?.data?.message || 'An error occurred');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Name:</label>
        <input type="text" name="name" value={petInfo.name} onChange={handleChange} />
      </div>
      <div>
        <label>Species:</label>
        <input type="text" name="species" value={petInfo.species} onChange={handleChange} />
      </div>
      <div>
        <label>Breed:</label>
        <input type="text" name="breed" value={petInfo.breed} onChange={handleChange} />
      </div>
      <div>
        <label>Age:</label>
        <input type="text" name="age" value={petInfo.age} onChange={handleChange} />
      </div>
      <div>
        <label>Medical History:</label>
        <textarea name="medicalHistory" value={petInfo.medicalHistory} onChange={handleChange}></textarea>
      </div>
      <button type="submit">Add Pet</button>
    </form>
  );
}

export default AddPetForm;
