import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { AnimatePresence, motion } from 'framer-motion';

// --- 1. Helper Functions ---
const formatTimeAgo = (date: Date | string | null | undefined) => {
  if (!date) return "Just now";
  try {
    const d = typeof date === 'string' ? new Date(date) : date;
    if (isNaN(d.getTime())) return "Recent";
    const seconds = Math.floor((new Date().getTime() - d.getTime()) / 1000);
    if (seconds < 60) return "Just now";
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    return d.toLocaleDateString();
  } catch (e) {
    return "Recent";
  }
};

const getAlertKey = (alert: any, index: number) => {
  return `${alert.type}-${alert.lat}-${alert.lng}-${index}`;
};

// --- 2. Types ---
interface DisasterAlert {
  type?: string;
  label?: string;
  lat?: number;
  lng?: number;
  intensity?: number;
  timestamp?: string | Date;
  riskLevel?: string;
}

// --- 3. AlertCard Component ---
const AlertCard: React.FC<{ alert: DisasterAlert; index: number }> = ({ alert, index }) => {
  return (
    <motion.div
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.05 }}
      className="p-3 border-b border-slate-800 bg-slate-900/30 mb-2 rounded-lg"
    >
      <div className="flex justify-between items-start mb-1">
        <span className="text-[10px] font-bold uppercase tracking-wider text-blue-400">
          {alert.type || 'ALERT'}
        </span>
        <span className="text-[9px] text-slate-500 font-mono">
          {formatTimeAgo(alert.timestamp)}
        </span>
      </div>
      <p className="text-xs text-slate-300 line-clamp-2">
        {alert.label || 'Monitoring signal detected'}
      </p>
    </motion.div>
  );
};

// --- 4. AlertsPanel Component ---
const AlertsPanel: React.FC<{ alerts: DisasterAlert[] }> = ({ alerts }) => {
  return (
    <div className="glass-card h-full flex flex-col border border-slate-800 rounded-xl bg-slate-950/50">
      <div className="p-4 border-b border-slate-800 flex items-center gap-2">
        <AlertTriangle className="w-5 h-5 text-red-500" />
        <h3 className="font-semibold text-slate-200">Live Alerts</h3>
      </div>
      <ScrollArea className="flex-1 p-4">
        <AnimatePresence>
          {alerts.map((alert, index) => (
            <AlertCard key={getAlertKey(alert, index)} alert={alert} index={index} />
          ))}
        </AnimatePresence>
      </ScrollArea>
    </div>
  );
};

export default AlertsPanel;
