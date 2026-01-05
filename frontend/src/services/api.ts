import { API_BASE_URL, API_ENDPOINTS } from '@/config/api';
import type { 
  PredictAllResponse, 
  ActiveAlertsResponse, 
  CriticalZonesResponse,
  AlertCreate,
  AlertResponse 
} from '@/types/api';

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Get all disaster predictions
  async getPredictions(): Promise<PredictAllResponse> {
    return this.request<PredictAllResponse>(API_ENDPOINTS.predictAll);
  }

  // Get active alerts
  async getActiveAlerts(): Promise<ActiveAlertsResponse> {
    return this.request<ActiveAlertsResponse>(API_ENDPOINTS.activeAlerts);
  }

  // Create a new alert
  async createAlert(alert: AlertCreate): Promise<{ status: string; alert_id: number }> {
    const params = new URLSearchParams({
      disaster_type: alert.disaster_type,
      location: `${alert.latitude},${alert.longitude}`,
      severity: alert.severity,
      population_at_risk: String(alert.population || 0),
    });
    
    return this.request(`${API_ENDPOINTS.createAlert}?${params}`, {
      method: 'POST',
    });
  }

  // Get critical zones for a disaster type
  async getCriticalZones(disasterType: string): Promise<CriticalZonesResponse> {
    return this.request<CriticalZonesResponse>(API_ENDPOINTS.criticalZones(disasterType));
  }

  // Health check
  async healthCheck(): Promise<{ message: string }> {
    return this.request('/');
  }
}

export const apiService = new ApiService(API_BASE_URL);
export default apiService;
