import React, { useState } from 'react';

function App() {
  const [statusUrl, setStatusUrl] = useState(null);
  const [status, setStatus] = useState(null);

  const startOrchestration = async () => {
    try {
      const baseUrl = process.env.REACT_APP_FUNCTION_URL || "";
      const response = await fetch(`${baseUrl}/api/orchestrators/hello_orchestrator`, { method: "POST" });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();

      const uri = new URL(result.statusQueryGetUri);
      setStatusUrl(uri.toString());
    } catch (error) {
      console.error("Failed to start orchestration:", error);
      alert("Failed to start orchestration. Please try again.");
    }
  };

  const checkStatus = async () => {
    if (!statusUrl) return;
    const response = await fetch(statusUrl);
    const result = await response.json();
    setStatus(result.runtimeStatus);
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">Durable Function Tester</h1>
      <button 
        data-testid="start-button" 
        onClick={startOrchestration} 
        className="bg-blue-500 text-white px-4 py-2 rounded mt-2"
      >
        Start Orchestration
      </button>
      {statusUrl && (
        <div className="mt-4" data-testid="status-section">
          <p>Status URL: <code data-testid="status-url">{statusUrl}</code></p>
          <button 
            data-testid="check-status-button"
            onClick={checkStatus} 
            className="bg-green-500 text-white px-4 py-2 rounded mt-2"
          >
            Check Status
          </button>
          {status && <p className="mt-2" data-testid="status-display">Status: {status}</p>}
        </div>
      )}
    </div>
  );
}

export default App;
