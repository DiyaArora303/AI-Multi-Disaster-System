import { useBackendData } from './use-backend-data'; 
import type { AlertResponse, PredictionResponse, PredictAllResponse } from '@/types/api';
import { DISASTER_TYPES } from '@/lib/constants'; 

// Helper to determine severity based on a prediction value (0.0 to 1.0)
const determineSeverity = (value: number): string => {
    if (value > 0.85) return 'critical';
    if (value > 0.65) return 'high';
    if (value > 0.35) return 'moderate';
    return 'low';
};

/**
 * Hook to fetch combined prediction results AND stats from the backend.
 */
export const usePredictions = () => {
    const { 
        data: rawData, 
        loading, 
        error, 
        refetch 
    } = useBackendData<PredictAllResponse>('/predict_all');
    
    const predictions: PredictionResponse[] = [];
    
    if (rawData) {
        const timestamp = new Date().toISOString();

        for (const type of DISASTER_TYPES) {
            const rawPredictionArray = (rawData as any)[type] || [];
            
            const representativeValue = rawPredictionArray.length > 0 
                ? rawPredictionArray.map((p: any) => {
                    if (typeof p === 'object' && p !== null && 'risk_score' in p) {
                        return p.risk_score / 100;
                    }
                    return Array.isArray(p) ? p[0] : (typeof p === 'number' ? p : 0);
                }).reduce((a: number, b: number) => Math.max(a, b), 0)
                : 0;

            predictions.push({
                disaster_type: type,
                probability: representativeValue,
                severity: determineSeverity(representativeValue),
                timestamp: timestamp,
                raw_data: rawPredictionArray,
            });
        }
    }

    return {
        data: { 
            predictions, 
            stats: rawData?.stats,
            heatmap: (rawData as any)?.heatmap || [] 
        }, 
        isLoading: loading,
        error: error,
        refetch: refetch
    };
};

/**
 * Hook to fetch all currently active alerts.
 */
export const useActiveAlerts = () => {
    const { 
        data: alertWrapper, 
        loading, 
        error, 
        refetch 
    } = useBackendData<any>('/active_alerts'); 
    
    const rawAlertsArray = alertWrapper?.alerts || [];
    
    const mappedAlerts: AlertResponse[] = rawAlertsArray.map((alert: any) => ({
        id: alert.id,
        disaster: alert.disaster_type, 
        location: alert.location,
        severity: alert.severity,
        population_at_risk: alert.population_at_risk,
        timestamp: alert.created_at || alert.timestamp,
    }));

    return {
        data: { alerts: mappedAlerts }, 
        isLoading: loading,
        error: error,
        refetch: refetch
    };
};