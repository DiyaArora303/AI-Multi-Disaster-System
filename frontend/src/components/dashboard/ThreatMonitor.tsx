import React from 'react';
import { Shield, AlertTriangle, CloudRain, Zap, Thermometer, Wind } from 'lucide-react';

interface ThreatMonitorProps {
  activeThreats?: string[];
}

const ThreatMonitor = ({ activeThreats = [] }: ThreatMonitorProps) => {
  const threats = [
    { id: 'flood', label: 'Flood', icon: CloudRain, color: 'text-blue-400' },
    { id: 'cyclone', label: 'Cyclone', icon: Wind, color: 'text-cyan-400' },
    { id: 'earthquake', label: 'Quake', icon: Zap, color: 'text-orange-400' },
    { id: 'landslide', label: 'Landslide', icon: Shield, color: 'text-amber-600' },
    { id: 'heatwave', label: 'Heat', icon: Thermometer, color: 'text-red-500' },
  ];

  return (
    <div className="glass-card p-4 h-full">
      <h3 className="text-xs font-black text-slate-500 uppercase tracking-widest mb-4">Threat Monitor</h3>
      <div className="grid grid-cols-2 gap-3">
        {threats.map((threat) => {
          // ✅ Ensure activeThreats exists
          const isActive = Array.isArray(activeThreats) && activeThreats.includes(threat.id);
          const Icon = threat.icon;

          return (
            <div 
              key={threat.id}
              className={`p-3 rounded-lg border flex flex-col items-center justify-center gap-2 transition-all ${
                isActive 
                ? 'bg-slate-800/50 border-primary/50 glow-primary' 
                : 'bg-slate-900/20 border-slate-800 opacity-40'
              }`}
            >
              <Icon className={`w-5 h-5 ${isActive ? threat.color : 'text-slate-600'}`} />
              <span className="text-[10px] font-bold uppercase tracking-tighter">{threat.label}</span>
              {isActive && (
                <span className="flex h-1.5 w-1.5 rounded-full bg-primary animate-pulse" />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ThreatMonitor;
