import React from 'react';
import { motion } from 'framer-motion';
import { RiskZone, riskColors, disasterIcons } from '@/types/disaster';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { MapPin, Users } from 'lucide-react';

interface RiskZonesListProps {
  zones: RiskZone[];
  onZoneClick?: (zone: RiskZone) => void;
}

const RiskZonesList: React.FC<RiskZonesListProps> = ({ zones, onZoneClick }) => {
  const sortedZones = [...zones].sort((a, b) => {
    const order = { critical: 0, high: 1, moderate: 2, low: 3, safe: 4 };
    return order[a.riskLevel] - order[b.riskLevel];
  });

  return (
    <div className="glass-card h-full flex flex-col">
      <div className="p-4 border-b border-border/50">
        <div className="flex items-center gap-2">
          <MapPin className="w-5 h-5 text-primary" />
          <h3 className="font-semibold text-foreground">Risk Zones</h3>
        </div>
      </div>

      <ScrollArea className="flex-1 p-4">
        <div className="space-y-2">
          {sortedZones.map((zone, index) => {
            const riskVariant = zone.riskLevel as 'critical' | 'high' | 'moderate' | 'low' | 'safe';
            
            return (
              <motion.div
                key={zone.id}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                whileHover={{ scale: 1.01 }}
                onClick={() => onZoneClick?.(zone)}
                className="flex items-center gap-3 p-3 rounded-lg bg-secondary/30 hover:bg-secondary/50 cursor-pointer transition-colors border border-transparent hover:border-border/50"
              >
                <div 
                  className="w-2 h-8 rounded-full"
                  style={{ backgroundColor: riskColors[zone.riskLevel] }}
                />
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-foreground text-sm">{zone.name}</span>
                    <Badge variant={riskVariant} className="text-[9px] px-1.5 py-0">
                      {zone.riskLevel.toUpperCase()}
                    </Badge>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground mt-0.5">
                    <span>{zone.state}</span>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <Users className="w-3 h-3" />
                      {(zone.population / 1000000).toFixed(1)}M
                    </span>
                  </div>
                </div>
                
                <div className="flex gap-1">
                  {zone.primaryThreats.slice(0, 2).map(threat => (
                    <span key={threat} className="text-sm">
                      {disasterIcons[threat]}
                    </span>
                  ))}
                </div>
              </motion.div>
            );
          })}
        </div>
      </ScrollArea>
    </div>
  );
};

export default RiskZonesList;
