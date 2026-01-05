// src/types/disaster.ts

export type DisasterType = 'flood' | 'cyclone' | 'earthquake' | 'landslide' | 'drought' | 'heatwave';

export type RiskLevel = 'critical' | 'high' | 'moderate' | 'low' | 'safe';

export interface DisasterAlert {
    id: string;
    type: DisasterType;
    title: string;
    location: string;
    state: string;
    riskLevel: RiskLevel;
    description: string;
    timestamp: Date;
    affectedPopulation: number;
    coordinates: [number, number];
}

export interface RiskZone {
    id: string;
    name: string;
    state: string;
    coordinates: [number, number];
    riskLevel: RiskLevel;
    primaryThreats: DisasterType[];
    population: number;
}

export interface DisasterStats {
    activeAlerts: number;
    criticalZones: number;
    affectedStates: number;
    populationAtRisk: number;
    predictedEvents24h: number;
    accuracy: number;
}

export const disasterIcons: Record<DisasterType, string> = {
    flood: '🌊',
    cyclone: '🌀',
    earthquake: '🔶',
    landslide: '⛰️',
    drought: '☀️',
    heatwave: '🔥',
};

export const riskColors: Record<RiskLevel, string> = {
    critical: '#ef4444',
    high: '#f97316',
    moderate: '#eab308',
    low: '#22c55e',
    safe: '#10b981',
};

export const disasterTypeLabels: Record<DisasterType, string> = {
    flood: 'Flood',
    cyclone: 'Cyclone',
    earthquake: 'Earthquake',
    landslide: 'Landslide',
    drought: 'Drought',
    heatwave: 'Heatwave',
};