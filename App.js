import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SmartRouteForm from './components/SmartRouteForm'; 


const handleSmartRouteSubmit = async (formData) => {
  try {
    const response = await fetch('http://localhost:8000/api/smart-route', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });

    const result = await response.json();
    console.log("Smart route result:", result);
  } catch (error) {
    console.error("Smart route error:", error);
  }
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SmartRouteForm onSubmit={handleSmartRouteSubmit} />} />
      </Routes>
    </Router>
  );
}

export default App;
