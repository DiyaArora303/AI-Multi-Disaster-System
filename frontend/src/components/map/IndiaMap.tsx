import React, { useEffect } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// Component to handle smooth camera transitions
const MapController = ({ focus }: { focus: [number, number] | null }) => {
  const map = useMap();
  useEffect(() => {
    if (focus) {
      map.flyTo(focus, 6, {
        duration: 1.5,
        easeLinearity: 0.25
      });
    }
  }, [focus, map]);
  return null;
};

interface HazardPoint {
  lat: number;
  lng: number;
  type: 'cyclone' | 'flood' | 'earthquake' | 'heatwave' | 'coldwave' | 'landslide';
  label: string;
  intensity: number;
  hourOffset: number;
}

interface IndiaMapProps {
  heatmap: HazardPoint[];
  focus: [number, number] | null;
  selectedHour: number;
}

const IndiaMap = ({ heatmap = [], focus = null, selectedHour = 0 }: IndiaMapProps) => {
  const colors: Record<string, string> = {
    cyclone: '#00e5ff',    // Cyan
    flood: '#2979ff',      // Blue
    earthquake: '#d500f9', // Purple
    heatwave: '#ff1744',   // Red
    coldwave: '#ffffff',   // White
    landslide: '#76ff03'   // Neon Green
  };

  // Filter data based on scroller's hour
  const filteredData = heatmap.filter((p) => p.hourOffset === selectedHour);

  return (
    <div className="relative w-full h-[600px] rounded-[2rem] overflow-hidden border border-slate-800 bg-slate-950 shadow-2xl group">
      {/* Dynamic CSS for Pulsing Animation */}
      <style>{`
        @keyframes alert-pulse {
          0% { fill-opacity: 0.4; stroke-width: 1; }
          50% { fill-opacity: 0.8; stroke-width: 2; }
          100% { fill-opacity: 0.4; stroke-width: 1; }
        }
        .hazard-marker {
          animation: alert-pulse 2s infinite ease-in-out;
        }
      `}</style>

      <MapContainer 
        center={[20, 78]} 
        zoom={4} 
        style={{ height: '100%', width: '100%' }} 
        zoomControl={false}
        attributionControl={false}
      >
        <TileLayer 
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" 
          opacity={0.9}
        />
        
        <MapController focus={focus} />

        {filteredData.map((p, i) => (
          <CircleMarker
            key={`${p.label}-${p.type}-${selectedHour}-${i}`}
            center={[p.lat, p.lng]}
            radius={8 + p.intensity * 20}
            pathOptions={{
              fillColor: colors[p.type] || '#fff',
              color: 'white',
              weight: 1,
              fillOpacity: 0.6,
              className: 'hazard-marker' // Applying the pulse animation
            }}
          >
            <Popup minWidth={150} className="custom-popup">
              <div className="p-2 font-mono bg-slate-900 text-white rounded-lg">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-[10px] font-black uppercase tracking-tighter" style={{ color: colors[p.type] }}>
                    ● {p.type} ALERT
                  </span>
                  <span className="text-[9px] text-slate-400">T+{p.hourOffset}H</span>
                </div>
                <h3 className="text-xs font-bold border-b border-slate-700 pb-1 mb-1">{p.label}</h3>
                <div className="flex justify-between items-center">
                  <span className="text-[9px] text-slate-500">INTENSITY</span>
                  <span className="text-[10px] font-bold">{(p.intensity * 100).toFixed(0)}%</span>
                </div>
                <div className="w-full bg-slate-800 h-1 mt-1 rounded-full overflow-hidden">
                  <div 
                    className="h-full transition-all duration-500" 
                    style={{ width: `${p.intensity * 100}%`, backgroundColor: colors[p.type] }}
                  />
                </div>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>

      {/* Map Overlay UI */}
      <div className="absolute top-6 left-6 z-[1000] pointer-events-none">
        <div className="bg-slate-950/80 backdrop-blur-md p-3 border border-slate-800 rounded-xl">
          <p className="text-[10px] font-mono text-blue-400 leading-tight tracking-widest uppercase font-bold">
            Live Surveillance Feedback
          </p>
          <p className="text-[8px] text-slate-500 font-mono">
            {filteredData.length} ACTIVE_NODES_FOUND
          </p>
        </div>
      </div>

      {/* Legend */}
      <div className="absolute top-6 right-6 z-[1000] p-5 bg-slate-950/90 border border-slate-700 rounded-2xl backdrop-blur-md shadow-2xl">
        <h4 className="text-[10px] font-black text-white mb-3 uppercase tracking-widest border-b border-slate-800 pb-2 flex items-center gap-2">
          <div className="w-1.5 h-1.5 bg-red-500 rounded-full animate-ping" />
          Hazard Classification
        </h4>
        <div className="space-y-2">
          {Object.entries(colors).map(([type, color]) => (
            <div key={type} className="flex items-center gap-3 text-[10px] text-slate-300 uppercase font-bold tracking-tight">
              <div 
                className="w-3 h-3 rounded-full border border-white/20 shadow-lg" 
                style={{ backgroundColor: color, boxShadow: `0 0 10px ${color}44` }} 
              />
              {type}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default IndiaMap;