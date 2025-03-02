import React, { useState } from 'react';

function App() {
  const [hashValue, setHashValue] = useState("");
  const [storeResult, setStoreResult] = useState("");
  const [verifyResult, setVerifyResult] = useState("");

  // URL API backend; bạn có thể lưu trong .env (REACT_APP_API_URL)
  const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";


  const handleStoreHash = async () => {
    try {
      const response = await fetch(`${API_URL}/storeHash`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ hash_value: hashValue })
      });
      const data = await response.json();
      setStoreResult(`Transaction Hash: ${data.tx_hash}`);
    } catch (error) {
      setStoreResult(`Error: ${error.message}`);
    }
  };
  
  

  const handleVerifyHash = async () => {
    try {
      const response = await fetch(`${API_URL}/verifyHash/${hashValue}`);
      const data = await response.json();
      setVerifyResult(data.exists ? "Hash exists on blockchain" : "Hash does not exist");
    } catch (error) {
      setVerifyResult(`Error: ${error.message}`);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Blockchain Data Provenance Dashboard</h1>
      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Enter hash (e.g., 0x...)"
          value={hashValue}
          onChange={(e) => setHashValue(e.target.value)}
          style={{ width: "400px", marginRight: "10px" }}
        />
        <button onClick={handleStoreHash}>Store Hash</button>
        <button onClick={handleVerifyHash} style={{ marginLeft: "10px" }}>Verify Hash</button>
      </div>
      {storeResult && <p><strong>Store Result:</strong> {storeResult}</p>}
      {verifyResult && <p><strong>Verify Result:</strong> {verifyResult}</p>}
    </div>
  );
}

export default App;
