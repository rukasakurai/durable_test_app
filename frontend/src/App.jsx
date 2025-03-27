import React, { useState } from 'react';

function App() {
  const [statusUrl, setStatusUrl] = useState(null);
  const [status, setStatus] = useState(null);

  const startOrchestration = async () => {
    try {
      const response = await fetch("/api/orchestrators/hello_orchestrator", { method: "POST" });
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
    const customStatusUrl = statusUrl.replace("/api/orchestrators/hello_orchestrator", "/api/status");
    const response = await fetch(customStatusUrl);
    const result = await response.json();
    setStatus(result.runtimeStatus);
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">Durable Function Tester</h1>
      <button onClick={startOrchestration} className="bg-blue-500 text-white px-4 py-2 rounded mt-2">
        Start Orchestration
      </button>
      {statusUrl && (
        <div className="mt-4">
          <p>Status URL: <code>{statusUrl}</code></p>
          <button onClick={checkStatus} className="bg-green-500 text-white px-4 py-2 rounded mt-2">
            Check Status
          </button>
          {status && <p className="mt-2">Status: {status}</p>}
        </div>
      )}
    </div>
  );
}

export default App;
