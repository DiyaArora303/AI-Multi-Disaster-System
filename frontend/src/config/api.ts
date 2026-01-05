// Backend API Configuration
// Change this to your actual backend URL when deploying
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
