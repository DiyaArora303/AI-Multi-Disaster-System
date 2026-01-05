import React, { useState } from 'react';
import { useBackendData } from '@/hooks/use-backend-data';
import Header from '@/components/layout/Header';
import { StatsOverview } from "@/components/dashboard/StatsOverview";
import IndiaMap from '@/components/map/IndiaMap';
import QuickActions from '@/components/dashboard/QuickActions';
import { Activity, Clock, Zap, X, ShieldAlert } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Index = () => {
  const { stats, heatmap, warroom_ticker, isConnected } = useBackendData();
  const [focus, setFocus] = useState<[number, number] | null>(null);
  const [hour, setHour] = useState(0);
  const [aiIntel, setAiIntel] = useState("");
  const [loadingAI, setLoadingAI] = useState(false);

  const displayAlerts = heatmap?.filter((p: any) => p.hourOffset === hour) || [];

  const getAIBriefing = async (hazard: any) => {
    setLoadingAI(true);
    setAiIntel("DECRYPTING NEURAL LINK...");
    try {
      const res = await fetch("http://localhost:8000/api/ai_briefing", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(hazard),
      });
      const json = await res.json();
      setAiIntel(json.intel);
    } catch (e) {
      setAiIntel("Uplink timeout. Check Command Backend.");
    } finally {
      setLoadingAI(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col overflow-hidden">
      <div className="p-6 space-y-6 flex-1 overflow-y-auto pb-24">
        {/* Header - Search isolated from Logo Refresh */}
        <Header onSearch={(coords: [number, number]) => setFocus(coords)} />
        
        <StatsOverview stats={stats} />
        
        {/* Quick Actions containing Sim Toggle */}
        <QuickActions />

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-8 relative rounded-[2.5rem] overflow-hidden border border-slate-800 bg-slate-900/20">
            <IndiaMap heatmap={heatmap} focus={focus} selectedHour={hour} />

            <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-[1000] w-[90%] bg-slate-900/90 p-6 rounded-3xl border border-slate-700 backdrop-blur-xl shadow-2xl">
              <div className="flex justify-between items-center mb-4">
                <span className="text-[10px] font-black text-blue-400 uppercase tracking-[0.2em]">Global Forecast</span>
                <div className="flex items-center gap-2">
                  <Clock size={16} className="text-blue-500" />
                  <span className="text-sm font-black text-white">PROJECTION: T + {hour}H</span>
                </div>
                <span className="text-[10px] font-black text-slate-500 uppercase">24H Window</span>
              </div>
              <input
                type="range" min="0" max="21" step="3"
                value={hour}
                onChange={(e) => setHour(parseInt(e.target.value))}
                className="w-full accent-blue-600 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
              />
            </div>
          </div>

          {/* Side Alerts Panel */}
          <div className="lg:col-span-4 bg-slate-900/40 border border-slate-800 rounded-[2.5rem] p-6 h-[600px] flex flex-col backdrop-blur-sm">
            <div className="flex items-center justify-between mb-6 border-b border-slate-800 pb-4">
              <div className="flex items-center gap-3">
                <Activity className="text-red-500 animate-pulse" />
                <h3 className="text-sm font-black uppercase">Live Intelligence</h3>
              </div>
              <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-emerald-500 shadow-[0_0_10px_#10b981]' : 'bg-red-500'}`} />
            </div>

            <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
              {displayAlerts.length > 0 ? displayAlerts.map((item: any, idx: number) => (
                <div
                  key={idx}
                  onClick={() => setFocus([item.lat, item.lng])}
                  className="p-5 bg-slate-950/80 border border-slate-800 rounded-2xl hover:border-blue-500/50 transition-all cursor-pointer group relative overflow-hidden"
                >
                  <div className="flex justify-between mb-3">
                    <span className={`text-[9px] px-2.5 py-1 rounded-full font-black tracking-widest ${
                      item.level === 'CRITICAL' ? 'bg-red-500/20 text-red-500 border border-red-500/30' : 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                    }`}>
                      {item.level}
                    </span>
                    <span className="text-[9px] text-slate-600 font-mono">T+{item.hourOffset}H</span>
                  </div>

                  <h4 className="text-xs font-black uppercase text-slate-200 group-hover:text-blue-400 transition-colors">
                    {item.label}: {item.type}
                  </h4>

                  <p className="text-[10px] text-slate-500 mt-2">
                    POPULATION AT RISK: <span className="text-slate-200 font-bold">{item.pop}</span>
                  </p>

                  <button
                    onClick={(e) => { e.stopPropagation(); getAIBriefing(item); }}
                    className="mt-4 w-full text-[10px] font-black bg-blue-600 hover:bg-blue-500 text-white py-2.5 rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg shadow-blue-500/10"
                  >
                    <Zap size={12} fill="currentColor" /> VIEW AI BRIEF
                  </button>
                </div>
              )) : (
                <div className="h-full flex flex-col items-center justify-center opacity-20 italic text-xs">
                  Scanning global sectors...
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* AI TACTICAL MODAL */}
      <AnimatePresence>
        {aiIntel && (
          <div className="fixed inset-0 bg-black/80 backdrop-blur-md z-[3000] flex items-center justify-center p-6">
            <motion.div 
              initial={{ scale: 0.9, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.9, opacity: 0, y: 20 }}
              className="w-full max-w-lg bg-slate-900 border border-blue-500/30 p-8 rounded-[2.5rem] shadow-[0_0_50px_rgba(59,130,246,0.2)] relative"
            >
              <button onClick={() => setAiIntel("")} className="absolute top-8 right-8 text-slate-500 hover:text-white transition-colors">
                <X size={20} />
              </button>
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-blue-500/20 rounded-lg text-blue-400">
                  <ShieldAlert size={20} />
                </div>
                <h4 className="text-blue-400 text-xs font-black uppercase tracking-[0.3em]">Tactical Intelligence Report</h4>
              </div>
              <p className="text-lg font-medium leading-relaxed text-slate-200 italic border-l-4 border-blue-600 pl-6 py-2">
                "{aiIntel}"
              </p>
              <button 
                onClick={() => setAiIntel("")}
                className="mt-10 w-full py-4 bg-blue-600 hover:bg-blue-500 rounded-2xl text-xs font-black uppercase tracking-widest transition-all text-white"
              >
                Acknowledge Directive
              </button>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* WAR ROOM TICKER */}
      <footer className="fixed bottom-0 left-0 w-full h-10 bg-black border-t border-slate-800 flex items-center overflow-hidden z-[4000]">
        <div className="bg-red-600 h-full px-8 flex items-center font-black italic z-10 skew-x-[-15deg] -translate-x-3">
           <span className="skew-x-[15deg] text-[10px] text-white tracking-tighter">LIVE_DATA_UPLINK</span>
        </div>
        <div className="flex whitespace-nowrap animate-marquee items-center gap-16 h-full">
            {warroom_ticker?.map((text: string, i: number) => (
              <span key={i} className="text-[10px] font-mono font-bold text-slate-400 uppercase">
                {text} <span className="text-red-500 mx-6 opacity-30">///</span>
              </span>
            ))}
            {/* Loop for infinite scroll */}
            {warroom_ticker?.map((text: string, i: number) => (
              <span key={`dup-${i}`} className="text-[10px] font-mono font-bold text-slate-400 uppercase">
                {text} <span className="text-red-500 mx-6 opacity-30">///</span>
              </span>
            ))}
        </div>
      </footer>

      <style>{`
        @keyframes marquee {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        .animate-marquee { animation: marquee 40s linear infinite; }
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 10px; }
      `}</style>
    </div>
  );
};

export default Index;