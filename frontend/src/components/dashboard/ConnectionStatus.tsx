import React from 'react';

interface ConnectionStatusProps {
  isConnected: boolean;
  isLoading: boolean;
}

const ConnectionStatus: React.FC<ConnectionStatusProps> = ({ isConnected, isLoading }) => {
  return (
    <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800">
      <div className={`h-2 w-2 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
      <span className="text-[10px] font-mono text-slate-300">
        {isLoading ? "SYNCING..." : isConnected ? "SYSTEM ONLINE" : "OFFLINE"}
      </span>
    </div>
  );
};

export default ConnectionStatus;
