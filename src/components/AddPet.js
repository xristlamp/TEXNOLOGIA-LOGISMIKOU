import axios from 'axios';
import { useState } from 'react';

function AddPetForm({ userId }) {
  const [name, setName] = useState('');
  const [species, setSpecies] = useState('');
  const [breed, setBreed] = useState('');
  const [age, setAge] = useState('');
  const [medicalHistory, setMedicalHistory] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`/api/users/${userId}/pets`, {
        name,
        species,
        breed,
        age,
        medicalHistory
      });
      alert(response.data.message);
    } catch (error) {
      alert(error.response?.data?.message || 'An error occurred');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Name:</label>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
      </div>
      <div>
        <label>Species:</label>
        <input type="text" value={species} onChange={(e) => setSpecies(e.target.value)} />
      </div>
      <div>
        <label>Breed:</label>
        <input type="text" value={breed} onChange={(e) => setBreed(e.target.value)} />
      </div>
      <div>
        <label>Age:</label>
        <input type="text" value={age} onChange={(e) => setAge(e.target.value)} />
      </div>
      <div>
        <label>Medical History:</label>
        <textarea value={medicalHistory} onChange={(e) => setMedicalHistory(e.target.value)}></textarea>
      </div>
      <button type="submit">Add Pet</button>
    </form>
  );
}

export default AddPetForm;
