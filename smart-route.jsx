import { useState } from "react";
import SmartRouteForm from "@/components/SmartRouteForm";

export default function SmartRoutePage() {
  const [responseData, setResponseData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFormSubmit = async (formData) => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/traffic/smart-routes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      setResponseData(data);
    } catch (error) {
      console.error("Error fetching smart routes:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Smart Route Planner</h1>
      <SmartRouteForm onSubmit={handleFormSubmit} />

      {loading && <p className="text-blue-500 mt-4">Loading...</p>}

      {responseData && (
        <div className="mt-6 border rounded p-4 shadow">
          <h2 className="text-xl font-semibold mb-2">🚍 Suggested Routes</h2>
          {responseData.map((route, index) => (
            <div key={index} className="mb-4 p-3 border rounded">
              <p><strong>Route ID:</strong> {route.route_id}</p>
              <p><strong>Path:</strong> {route.path.join(" → ")}</p>
              <p><strong>ETA:</strong> {route.estimated_time} mins</p>
              <p><strong>Reason:</strong> {route.reason}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
