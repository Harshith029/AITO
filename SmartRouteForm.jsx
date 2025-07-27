import React, { useState, useEffect } from 'react';
import './SmartRouteForm.css';

const SmartRouteForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    source: '',
    destination: '',
    time: '',
    preference: 'fastest',
    notes: ''
  });

  const [errors, setErrors] = useState({});
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    if (formSubmitted && Object.keys(errors).length === 0) {
      setSummary({ ...formData });
    }
  }, [formSubmitted, errors]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.source.trim()) newErrors.source = 'Source is required';
    if (!formData.destination.trim()) newErrors.destination = 'Destination is required';
    if (!formData.time) newErrors.time = 'Time is required';
    if (!/^\d{2}:\d{2}$/.test(formData.time)) newErrors.time = 'Time format must be HH:MM';
    return newErrors;
  };

  const handleSubmit = async(e) => {
    e.preventDefault();
    const newErrors = validate();
    setErrors(newErrors);
    setFormSubmitted(true);

   if (Object.keys(newErrors).length === 0) {
  try {
    const response = await fetch("http://localhost:8000/api/smart-route", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(formData)
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    console.log("Backend response:", data); 
  } catch (error) {
    console.error("Error submitting to backend:", error);
  }

  onSubmit(formData); 
}

  };

  const resetForm = () => {
    setFormData({
      source: '',
      destination: '',
      time: '',
      preference: 'fastest',
      notes: ''
    });
    setErrors({});
    setSummary(null);
    setFormSubmitted(false);
  };

  const getDummySuggestions = (query) => {
    if (!query) return [];
    const all = ['Secunderabad', 'Ameerpet', 'Koti', 'Miyapur', 'Hitech City', 'LB Nagar', 'Charminar'];
    return all.filter(place => place.toLowerCase().includes(query.toLowerCase()));
  };

  const sourceSuggestions = getDummySuggestions(formData.source);
  const destinationSuggestions = getDummySuggestions(formData.destination);

  return (
    <div className="smart-route-form">
      <h2>Plan Your Smart Route</h2>
      <form onSubmit={handleSubmit} noValidate>
        <div className="form-group">
          <label htmlFor="source">From:</label>
          <input
            id="source"
            type="text"
            name="source"
            placeholder="Start location"
            value={formData.source}
            onChange={handleChange}
            autoComplete="off"
          />
          {errors.source && <span className="error">{errors.source}</span>}
          <ul className="suggestions">
            {sourceSuggestions.map((s, i) => (
              <li key={i} onClick={() => setFormData({ ...formData, source: s })}>{s}</li>
            ))}
          </ul>
        </div>

        <div className="form-group">
          <label htmlFor="destination">To:</label>
          <input
            id="destination"
            type="text"
            name="destination"
            placeholder="Destination"
            value={formData.destination}
            onChange={handleChange}
            autoComplete="off"
          />
          {errors.destination && <span className="error">{errors.destination}</span>}
          <ul className="suggestions">
            {destinationSuggestions.map((s, i) => (
              <li key={i} onClick={() => setFormData({ ...formData, destination: s })}>{s}</li>
            ))}
          </ul>
        </div>

        <div className="form-group">
          <label htmlFor="time">Time of Travel:</label>
          <input
            id="time"
            type="time"
            name="time"
            value={formData.time}
            onChange={handleChange}
          />
          {errors.time && <span className="error">{errors.time}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="preference">Preference:</label>
          <select
            id="preference"
            name="preference"
            value={formData.preference}
            onChange={handleChange}
          >
            <option value="fastest">Fastest Route</option>
            <option value="least_crowded">Least Crowded</option>
            <option value="scenic">Scenic</option>
            <option value="bus_only">TSRTC Bus Only</option>
          </select>
        </div>

        <div className="form-group">
          <label>
            Extra Notes:
            <textarea
              name="notes"
              value={formData.notes || ''}
              onChange={handleChange}
              placeholder="Optional instructions or comments..."
            />
          </label>
        </div>

        <div className="button-group">
          <button type="submit">Get Smart Route</button>
          <button type="button" onClick={resetForm}>Reset</button>
        </div>
      </form>

      {summary && (
        <div className="summary-box">
          <h3>Submission Summary</h3>
          <p><strong>From:</strong> {summary.source}</p>
          <p><strong>To:</strong> {summary.destination}</p>
          <p><strong>Time:</strong> {summary.time}</p>
          <p><strong>Preference:</strong> {summary.preference}</p>
          {summary.notes && <p><strong>Notes:</strong> {summary.notes}</p>}
        </div>
      )}
    </div>
  );
};

export default SmartRouteForm;
