// frontend/src/config/api.ts

export const API_BASE = 
  import.meta.env.VITE_API_URL || 
  "https://ai-multi-disaster-prediction-system.onrender.com";

export const API_ENDPOINTS = {
  // Predictions
  predictAll: '/api/predict_all',
  
  // Individual disaster predictions
  flood: '/api/flood',
  cyclone: '/api/cyclone',
  earthquake: '/api/earthquake',
  landslide: '/api/landslide',
  heatwave: '/api/heatwave',
  
  // Alerts
  activeAlerts: '/api/active_alerts',
  createAlert: '/api/create_alert',
  
  // Zones
  criticalZones: (disasterType: string) => `/api/critical_zones/${disasterType}`,
  
  // Population
  population: '/api/population',
} as const;
