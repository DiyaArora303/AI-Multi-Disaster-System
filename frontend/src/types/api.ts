// src/types/api.ts

// --- RAW BACKEND DATA STRUCTURES ---

// 1. Raw Prediction Data (From GET /api/predict_all)
export interface BackendPredictionData {
    cyclone: number[];
    flood: number[];
    earthquake: number[];
    landslide: number[];
    heatwave: number[];
    drought?: number[];
}

// 2. Raw Alert Data (From GET /api/active_alerts)
export interface RawAlertData {
    id: number;
    disaster_type: string; // Backend field
    location: string;
    severity: 'low' | 'medium' | 'high' | 'extreme';
    population_at_risk: number;
    created_at: string; // Backend field
}

// --- HOOK RESPONSE TYPES ---

export type PredictAllResponse = BackendPredictionData;
export type ActiveAlertsResponse = RawAlertData[]; 

// --- STRUCTURED DATA (Expected by dataTransformers.ts) ---

// 3. Structured Alert Response 
export interface AlertResponse {
    id: number;
    disaster: string; // Transformed key
    location: string;
    severity: string;
    population_at_risk: number;
    timestamp: string; // Transformed key
}

// 4. Structured Prediction Response 
export interface PredictionResponse {
    disaster_type: string;
    severity: string;
    probability: number;
    timestamp: string;
    raw_data?: number[] | number[][];
}