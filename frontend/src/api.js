// api.js - Centralized API configuration

// Get API URL from runtime config, environment variables, or fallback
export const API_URL = 
  (window.RUNTIME_CONFIG && window.RUNTIME_CONFIG.API_URL) || 
  import.meta.env.VITE_API_URL || 
  'http://localhost:5001';

console.log(`Using API URL: ${API_URL}`);
