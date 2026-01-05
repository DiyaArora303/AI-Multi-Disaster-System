// src/data/mockData.ts

export const mockAlerts = [
    { id: 'm1', type: 'flood', title: 'Mock Flood', location: 'Coastal Area', state: 'MH', riskLevel: 'high', affectedPopulation: 12000, timestamp: new Date(), description: 'Mock alert description', coordinates: [19.0760, 72.8777] },
    { id: 'm2', type: 'cyclone', title: 'Mock Cyclone', location: 'Bay of Bengal', state: 'WB', riskLevel: 'critical', affectedPopulation: 50000, timestamp: new Date(), description: 'Mock alert description', coordinates: [22.5726, 88.3639] },
];

export const mockRiskZones = [
    { id: 'z1', name: 'West Coast Zone', state: 'GJ/MH', coordinates: [21.5, 74.0], riskLevel: 'moderate', primaryThreats: ['flood', 'cyclone'], population: 5000000 },
    { id: 'z2', name: 'East Delta Region', state: 'WB/OD', coordinates: [20.0, 86.0], riskLevel: 'high', primaryThreats: ['cyclone', 'heatwave'], population: 8000000 },
];

export const mockStats = {
    activeAlerts: 2,
    criticalZones: 1,
    affectedStates: 5,
    populationAtRisk: 120000,
    predictedEvents24h: 7,
    accuracy: 94.7,
};