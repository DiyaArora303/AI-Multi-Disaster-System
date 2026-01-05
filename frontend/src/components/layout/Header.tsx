import React, { useState, useEffect, useRef } from 'react';
import { Search, MapPin, CheckCircle2 } from 'lucide-react';

interface HeaderProps {
  onSearch: (coords: [number, number]) => void;
}

const Header = ({ onSearch }: HeaderProps) => {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const hubs: { [key: string]: [number, number] } = {
    "Mumbai": [19.07, 72.87], "Delhi": [28.61, 77.20], "Nagpur": [21.14, 79.08],
    "Kochi": [9.93, 76.26], "Tokyo": [35.67, 139.65], "London": [51.50, -0.12],
    "New York": [40.71, -74.00], "Sydney": [-33.86, 151.20]
  };

  useEffect(() => {
    if (query.length > 0) {
      const filtered = Object.keys(hubs).filter(city => 
        city.toLowerCase().startsWith(query.toLowerCase())
      );
      setSuggestions(filtered);
      setShowDropdown(true);
    } else {
      setShowDropdown(false);
    }
  }, [query]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const coords = hubs[query];
    if (coords) onSearch(coords);
    setShowDropdown(false);
  };

  return (
    // 'gap-10' and 'justify-between' ensure the Search Bar stays away from the Logo
    <header className="flex flex-col md:flex-row items-center justify-between gap-10 mb-10 px-4 w-full">
      
      {/* BRAND SECTION: Refresh logic is now ONLY inside this DIV */}
      <div 
        onClick={() => window.location.reload()} 
        className="flex items-center gap-4 cursor-pointer group min-w-max hover:opacity-80 transition-all"
      >
        <div className="p-3 bg-blue-600 rounded-2xl shadow-lg group-hover:rotate-12 transition-transform">
          <MapPin className="text-white" size={24} />
        </div>
        <div className="flex flex-col">
          <h1 className="text-2xl font-black tracking-tighter text-white leading-none">
            DRISHTI<span className="text-blue-500">.AI</span>
          </h1>
          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.3em]">Global Command</span>
        </div>
      </div>

      {/* SEARCH SECTION: Isolated from the refresh click */}
      <div className="relative w-full max-w-xl" ref={dropdownRef}>
        <form onSubmit={handleSearchSubmit} className="relative group">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-blue-400 transition-colors" size={18} />
          <input 
            type="text"
            value={query}
            autoComplete="off"
            // Typing now works perfectly because this input is not inside a 'refresh' div
            onChange={(e) => setQuery(e.target.value)} 
            placeholder="Search global hubs (e.g. Mumbai)..."
            className="w-full bg-slate-900 border border-slate-800 text-sm py-4 pl-12 pr-4 rounded-2xl focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 transition-all text-slate-200"
          />
        </form>

        {showDropdown && suggestions.length > 0 && (
          <div className="absolute top-full left-0 w-full mt-2 bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden z-[5000] shadow-2xl">
            {suggestions.map((city) => (
              <div 
                key={city}
                onClick={() => {
                  setQuery(city);
                  onSearch(hubs[city]);
                  setShowDropdown(false);
                }}
                className="px-5 py-3 text-sm text-slate-300 hover:bg-blue-600 hover:text-white cursor-pointer flex justify-between items-center transition-colors"
              >
                <span>{city}</span>
                <span className="text-[10px] opacity-30 font-mono">NODE_SELECT</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* STATUS SECTION: Balances the UI layout */}
      <div className="hidden lg:flex items-center gap-6 min-w-max">
        <div className="flex flex-col items-end">
          <div className="flex items-center gap-2 text-emerald-500">
            <CheckCircle2 size={14} />
            <span className="text-[10px] font-black uppercase tracking-widest">Uplink Active</span>
          </div>
          <span className="text-[9px] font-mono text-slate-600 tracking-tighter">ENCRYPTED_SESSION</span>
        </div>
      </div>
    </header>
  );
};

export default Header;