"use client";

import { useState } from 'react';
import axios from 'axios';

type Props = {
  onAddName: (name: string) => void;
};

export default function InputForm({ onAddName }: Props) {
  const [name, setName] = useState('');

  const handleSubmit = () => {
    if (!name.trim()) return;

    // axios.post('http://localhost:5000/api/data', { name })
    axios.post('/api/data', { name })
      .then(() => {
        onAddName(name);
        setName('');
      })
      .catch(error => {
        console.error('Error adding name:', error);
      });
  };

  return (
    <div className="mb-4">
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter your name"
        className="border rounded px-3 py-2 mr-2"
      />
      <button
        onClick={handleSubmit}
        className="bg-blue-500 text-white rounded px-4 py-2 hover:bg-blue-700"
      >
        Add Name
      </button>
    </div>
  );
}