import React from 'react';
import { toast } from "sonner";
import { Users, MapPin, AlertCircle, ShieldCheck } from 'lucide-react';

export const StatsOverview = ({ stats }: any) => {
  const showDetail = (title: string, list: string[]) => {
    if (!list || list.length === 0) return toast.info(`No active incidents detected.`);
    toast(title, {
      description: (
        <div className="mt-2 space-y-1 max-h-48 overflow-y-auto">
          {list.map((item, i) => (
            <div key={i} className="text-[10px] font-mono border-l-2 border-primary pl-2 bg-slate-800/50 py-1 uppercase">{item}</div>
          ))}
        </div>
      )
    });
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div onClick={() => showDetail("Affected Regions", stats.affected_states)} className="glass-card p-4 cursor-pointer hover:border-blue-500 border border-slate-800 transition-all">
        <MapPin className="text-blue-500 mb-2" size={20} />
        <p className="text-[10px] uppercase font-bold text-slate-500">Active States</p>
        <h3 className="text-2xl font-black">{stats.affected_states?.length || 0}</h3>
      </div>
      <div onClick={() => showDetail("Active Threats", stats.critical_zones)} className="glass-card p-4 cursor-pointer hover:border-red-500 border border-slate-800 transition-all">
        <AlertCircle className="text-red-500 mb-2" size={20} />
        <p className="text-[10px] uppercase font-bold text-slate-500">Live Incidents</p>
        <h3 className="text-2xl font-black">{stats.critical_zones?.length || 0}</h3>
      </div>
      <div className="glass-card p-4 border border-slate-800">
        <Users className="text-emerald-500 mb-2" size={20} />
        <p className="text-[10px] uppercase font-bold text-slate-500">Population at Risk</p>
        <h3 className="text-2xl font-black">{stats.total_affected_population_M || 0}M</h3>
      </div>
      <div className="glass-card p-4 border border-slate-800">
        <ShieldCheck className="text-primary mb-2" size={20} />
        <p className="text-[10px] uppercase font-bold text-slate-500">AI Precision</p>
        <h3 className="text-2xl font-black">{stats.ai_accuracy_percent}%</h3>
      </div>
    </div>
  );
};

export default StatsOverview;