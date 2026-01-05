import type { AlertResponse, PredictionResponse } from '@/types/api';
import type { DisasterAlert, DisasterType, RiskZone, DisasterStats, RiskLevel } from '@/types/disaster';

function mapSeverityToRiskLevel(severity: string | null | undefined): RiskLevel {
    const s = severity?.toLowerCase();
    if (s === 'critical' || s === 'extreme') return 'critical';
    if (s === 'high' || s === 'severe') return 'high';
    if (s === 'moderate' || s === 'medium') return 'moderate';
    return s === 'low' ? 'low' : 'safe';
}

function mapDisasterType(type: string | null | undefined): DisasterType {
    const normalized = type?.toLowerCase();
    const valid: DisasterType[] = ['flood', 'cyclone', 'earthquake', 'landslide', 'drought', 'heatwave'];
    return valid.includes(normalized as DisasterType) ? (normalized as DisasterType) : 'flood';
}

export function transformAlert(alert: AlertResponse): DisasterAlert {
    const pop = alert.population_at_risk ?? 0;
    return {
        id: String(alert.id),
        type: mapDisasterType(alert.disaster),
        title: `${alert.disaster || 'Disaster'} Alert`,
        location: alert.location?.split(',')[0] || 'Unknown',
        state: 'India', 
        riskLevel: mapSeverityToRiskLevel(alert.severity),
        description: `${alert.severity} alert. Population: ${pop.toLocaleString()}`,
        timestamp: new Date(alert.timestamp),
        affectedPopulation: pop,
        coordinates: [78.9629, 20.5937],
    };
}

export function transformPredictionToAlert(prediction: PredictionResponse, index: number): DisasterAlert {
    return {
        id: `pred-${index}`,
        type: mapDisasterType(prediction.disaster_type),
        title: `${prediction.disaster_type} Prediction`,
        location: prediction.location_name || 'Predicted Zone',
        state: 'India',
        riskLevel: mapSeverityToRiskLevel(prediction.risk_level),
        description: `Probability: ${prediction.probability ? (Number(prediction.probability) * 100).toFixed(1) : '0'}%`,
        timestamp: new Date(),
        affectedPopulation: Number(prediction.population_at_risk) || 0,
        coordinates: [78.9629, 20.5937],
    };
}

export function calculateStats(alerts: DisasterAlert[], predictions: any[]): DisasterStats {
    return {
        activeAlerts: alerts.length,
        criticalZones: alerts.filter(a => a.riskLevel === 'critical').length,
        affectedStates: 1,
        populationAtRisk: "0.0M",
        predictedEvents24h: predictions.length,
        accuracy: 92.5,
    };
}

export function updateRiskZonesFromPredictions(baseZones: RiskZone[], predictions: any[]): RiskZone[] {
    return predictions.map((p, i) => ({
        id: `zone-${i}`,
        name: p.location_name || 'Active Zone',
        state: 'IN',
        coordinates: [78.9629, 20.5937],
        riskLevel: mapSeverityToRiskLevel(p.risk_level),
        population: Number(p.population_at_risk) || 0,
        activeThreats: [mapDisasterType(p.disaster_type)]
    }));
}