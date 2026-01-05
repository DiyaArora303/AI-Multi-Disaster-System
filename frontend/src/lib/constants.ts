// src/lib/constants.ts

export const API_BASE_URL = 'http://127.0.0.1:8000/api';

export const DISASTER_TYPES = [
    'cyclone',
    'flood',
    'earthquake',
    'landslide',
    'heatwave',
    'drought'
] as const;

export type DisasterType = typeof DISASTER_TYPES[number];