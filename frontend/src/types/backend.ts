// src/types/backend.ts

// --- 1. Raw Prediction Data from GET /api/predict_all ---
// This directly maps the dictionary structure returned by your FastAPI endpoint.
export interface BackendPredictionData {
    // Each key holds an array of prediction values (which the frontend then calculates risk from)
    cyclone: number[];
    flood: number[];
    earthquake: number[];
    landslide: number[];
    heatwave: number[];
    drought?: number[]; // Include 'drought' if the backend ever adds it
}

// --- 2. Raw Alert Data from GET /api/active_alerts ---
// This represents a single record returned by your database/alerts router.
export interface RawAlertData {
    id: number;
    // Note: The backend returns 'disaster_type' and 'created_at'.
    // We use a flexible type here as the transformer handles mapping this to the frontend model.
    disaster_type: string; 
    location: string;
    severity: 'low' | 'medium' | 'high' | 'extreme';
    population_at_risk: number;
    created_at: string; // ISO date string
}

// --- 3. Unified Types for useApi.ts ---
// These are used as the generic type <T> in use-backend-data.tsx

/**
 * Type used by usePredictions. It matches the structure of BackendPredictionData.
 */
export type PredictAllResponse = BackendPredictionData;

/**
 * Type used by useActiveAlerts. It is an array of the raw alert objects.
 */
export type ActiveAlertsResponse = RawAlertData[];