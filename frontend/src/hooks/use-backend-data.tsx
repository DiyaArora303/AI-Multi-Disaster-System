import { useState, useEffect } from 'react';

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
    warroom_ticker: [], // ✅ ADDED (no existing field changed)
    activeThreats: [], 
    loading: true, 
    isConnected: false, 
    lastUpdated: ""
  });

  const fetchUpdate = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/predict_all/stats");
      if (!res.ok) throw new Error("Connection failed");
      const json = await res.json();

      setData({
        stats: json.stats,
        heatmap: json.heatmap || [],
        warroom_ticker: json.warroom_ticker || [], // ✅ ADDED mapping only
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
