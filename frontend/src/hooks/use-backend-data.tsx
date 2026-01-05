import { useState, useEffect } from 'react';
import { API_BASE } from '@/config/api';

export function useBackendData() {
  const [data, setData] = useState({
    stats: { 
      active_alert_count: 0, 
      total_affected_population_M: 0, 
      affected_states: [], 
      critical_zones: [], 
      ai_accuracy_percent: 94.2 
    },
    heatmap: [],
    warroom_ticker: [], 
    activeThreats: [], 
    loading: true, 
    isConnected: false, 
    lastUpdated: ""
  });

  const fetchUpdate = async () => {
    try {
      // ✅ UPDATED: Uses Config URL
      const res = await fetch(`${API_BASE}/api/predict_all/stats`);
      if (!res.ok) throw new Error("Connection failed");
      const json = await res.json();

      setData({
        stats: json.stats,
        heatmap: json.heatmap || [],
        warroom_ticker: json.warroom_ticker || [],
        activeThreats: json.activeThreats || [],
        loading: false,
        isConnected: true,
        lastUpdated: json.last_updated
      });
    } catch (e) {
      setData(prev => ({ ...prev, loading: false, isConnected: false }));
    }
  };

  useEffect(() => {
    fetchUpdate();
    const interval = setInterval(fetchUpdate, 5000);
    return () => clearInterval(interval);
  }, []);

  return data;
}