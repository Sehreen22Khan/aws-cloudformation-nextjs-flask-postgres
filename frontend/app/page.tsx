"use client";

import axios from 'axios';
import { useEffect, useState } from 'react';
import InputForm from './components/InputForm';
import NameList from './components/NameList';

export default function HomePage() {
  const [data, setData] = useState<{ id: number; name: string }[]>([]);

  useEffect(() => {
    axios.get('http://localhost:5000/api/data')
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  const handleAddName = (name: string) => {
    setData(prevData => [...prevData, { id: prevData.length + 1, name }]);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6">
      <h1 className="text-2xl font-bold mb-4">Welcome to the Fun App!</h1>
      <InputForm onAddName={handleAddName} />
      <NameList data={data} />
    </div>
  );
}
