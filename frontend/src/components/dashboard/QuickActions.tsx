import React from 'react';
import { AlertCircle, Zap, Radio, Bell, Play } from 'lucide-react';
import { toast } from 'sonner';

const QuickActions = () => {
  const dispatchAlert = async (level: string, message: string) => {
    try {
      const response = await fetch('http://localhost:8000/api/trigger_alert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ level, message }),
      });
      if (response.ok) {
        toast.success(`${level} DISPATCHED`, {
          description: "Makers have been notified via secure email.",
        });
      }
    } catch (e) {
      toast.error("UPLINK FAILED");
    }
  };

  const toggleSimMode = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/toggle_simulation", {
        method: "POST",
      });
      const json = await res.json();
      toast.info(
        json.simulation_active
          ? "SIMULATION LINK ACTIVE"
          : "REAL-TIME FEED RESTORED"
      );
    } catch (e) {
      toast.error("SIM MODE TOGGLE FAILED");
    }
  };

  const actions = [
    {
      label: 'Issue Alert',
      icon: AlertCircle,
      color: 'text-amber-500',
      action: () =>
        dispatchAlert(
          "SOFT ALERT",
          "General caution issued for regional monitoring."
        ),
    },
    {
      label: 'Emergency',
      icon: Zap,
      color: 'text-red-500',
      action: () =>
        dispatchAlert(
          "EMERGENCY",
          "Immediate threat detected! Urgent intervention required."
        ),
    },
    {
      label: 'Broadcast',
      icon: Radio,
      color: 'text-blue-500',
      action: () =>
        dispatchAlert(
          "BROADCAST",
          "Global system-wide broadcast sequence initiated."
        ),
    },
    {
      label: 'Notify',
      icon: Bell,
      color: 'text-emerald-500',
      action: () =>
        dispatchAlert("PING", "Developer system ping."),
    },
    {
      label: 'Sim Mode',
      icon: Play,
      color: 'text-pink-500',
      action: toggleSimMode,
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {actions.map((act) => (
        <button
          key={act.label}
          onClick={act.action}
          className="flex items-center gap-4 p-4 bg-slate-900/50 border border-slate-800 rounded-2xl hover:bg-slate-800 transition-all"
        >
          <act.icon className={act.color} size={24} />
          <span className="text-xs font-black uppercase tracking-widest text-slate-300">
            {act.label}
          </span>
        </button>
      ))}
    </div>
  );
};

export default QuickActions;
