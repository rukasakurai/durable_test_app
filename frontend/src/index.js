import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const API_BASE_URL = "https://your-custom-domain.com/api";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
