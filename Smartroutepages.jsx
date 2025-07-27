import React, { useState } from 'react';
import SmartRouteForm from '../components/SmartRouteForm';

const SmartRoutePage = () => {
  const [smartRoutes, setSmartRoutes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFormSubmit = async (formData) => {
    setLoading(true);
    setError('');
    setSmartRoutes(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/smart-route', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Unknown error occurred');
      }

      const data = await response.json();
      setSmartRoutes(data.routes);
    } catch (err) {
      setError(`Failed to fetch smart routes: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-center mb-6">AITO - Smart Route Planner</h1>
      <SmartRouteForm onSubmit={handleFormSubmit} />
      {loading && <p className="text-blue-500 mt-4">Generating routes...</p>}
      {error && <p className="text-red-500 mt-4">{error}</p>}
      {smartRoutes && (
        <div className="mt-6 p-4 bg-gray-100 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2">Optimized Routes</h2>
          <ul className="list-disc list-inside space-y-1">
            {smartRoutes.map((route, idx) => (
              <li key={idx}>{route}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default SmartRoutePage;
