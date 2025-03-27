import React, { useState } from 'react';

function App() {
  const [statusUrl, setStatusUrl] = useState(null);
  const [status, setStatus] = useState(null);

  const rewriteUrl = (url) => {
    const uri = new URL(url);
    uri.hostname = window.location.hostname;
    uri.protocol = window.location.protocol;
    return uri.toString();
  };

  const startOrchestration = async () => {
    const response = await fetch("/api/orchestrators/Hello", { method: "POST" });
    const result = await response.json();

    const rewrittenStatusQueryGetUri = rewriteUrl(result.statusQueryGetUri);
    setStatusUrl(rewrittenStatusQueryGetUri);
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
