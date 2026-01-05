import { useState } from "react";
import { Search } from "lucide-react";

export const SearchBar = () => {
  const [query, setQuery] = useState("");

  const search = async () => {
    if (!query) return;
    const res = await fetch(`http://127.0.0.1:8000/api/search?q=${query}`);
    const data = await res.json();
    alert(`${data.location.name}\nRisk: ${data.risk_percent}%`);
  };

  return (
    <div className="flex items-center gap-2 bg-slate-900 px-3 py-1 rounded-lg">
      <Search className="w-4 h-4 text-slate-400" />
      <input
        className="bg-transparent outline-none text-sm"
        placeholder="Search city/state..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && search()}
      />
    </div>
  );
};
