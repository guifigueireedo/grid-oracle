"use client";

import { ChevronRight, Trophy, AlertTriangle, Cpu, MapPin, Clock } from "lucide-react";
import { useState, useEffect } from "react";

// --- TEAM COLORS DICTIONARY ---
const driverColors: Record<string, string> = {
  "LANDO NORRIS": "#F47600",
  "MAX VERSTAPPEN": "#4781D7",
  "GABRIEL BORTOLETO": "#F50537",
  "ISACK HADJAR": "#4781D7",
  "PIERRE GASLY": "#00A1E8",
  "SERGIO PEREZ": "#909090",
  "KIMI ANTONELLI": "#00D7B6",
  "FERNANDO ALONSO": "#229971",
  "CHARLES LECLERC": "#ED1131",
  "LANCE STROLL": "#229971",
  "ALEXANDER ALBON": "#1868DB",
  "NICO HULKENBERG": "#F50537",
  "LIAM LAWSON": "#6C98FF",
  "ESTEBAN OCON": "#9C9FA2",
  "ARVID LINDBLAD": "#6C98FF",
  "FRANCO COLAPINTO": "#00A1E8",
  "LEWIS HAMILTON": "#ED1131",
  "CARLOS SAINZ": "#1868DB",
  "GEORGE RUSSELL": "#00D7B6",
  "VALTTERI BOTTAS": "#909090",
  "OSCAR PIASTRI": "#F47600",
  "OLIVER BEARMAN": "#9C9FA2"
};

interface DriverResult {
  name: string;
  position: number | "DNF";
  gap?: string;
  explanation?: string;
}

interface RaceEvent {
  id: string;
  name: string;
  location: string;
  date: string;
  date_start_utc?: string;
  circuit_image?: string;
  country_flag?: string;
  status: "cancelled" | "completed" | "next" | "future";
  results?: DriverResult[];
  predictions?: DriverResult[];
}

export default function RaceCard({ race }: { race: RaceEvent }) {
  const [isOpen, setIsOpen] = useState(false);
  const [localTime, setLocalTime] = useState<string>("Calculating...");

  useEffect(() => {
    if (race.date_start_utc) {
      const date = new Date(race.date_start_utc);
      setLocalTime(new Intl.DateTimeFormat('en-US', { weekday: 'short', hour: 'numeric', minute: '2-digit', timeZoneName: 'short' }).format(date));
    } else {
      setLocalTime("TBA");
    }
  }, [race.date_start_utc]);

  const isNext = race.status === "next";
  const isCompleted = race.status === "completed";
  const isCancelled = race.status === "cancelled";

  const displayData = isNext ? race.predictions : race.results;
  const col1 = displayData?.slice(0, 8) || [];
  const col2 = displayData?.slice(8, 16) || [];
  const col3 = displayData?.slice(16) || [];

  return (
    <div 
      // MOBILE FIX: Uses 85vw on mobile so it always fits nicely with margins, then jumps to fixed pixels on desktop.
      className={`transition-all duration-500 ease-in-out bg-oracle-dark border rounded-xl p-6 relative flex flex-col md:flex-row gap-6 overflow-hidden group snap-start
        ${isOpen ? "w-[85vw] max-w-[380px] md:max-w-none md:w-[1100px]" : "w-[85vw] max-w-[380px] md:max-w-none md:w-[400px]"}
        ${isNext ? "border-oracle-red shadow-red-glow" : "border-white/5"}
        ${isCancelled ? "opacity-50 grayscale" : ""}
      `}
    >
      {/* LEFT PANE */}
      <div className="w-full md:w-[352px] shrink-0 flex flex-col min-h-[450px] relative z-10">
        {race.circuit_image && (
          <div className="absolute top-10 -right-10 w-48 opacity-10 pointer-events-none transition-transform duration-500 group-hover:scale-110">
            <img src={race.circuit_image} alt="Circuit" className="w-full h-full object-contain filter invert" />
          </div>
        )}

        <div className="flex justify-between items-start mb-4">
          <div className="flex items-center gap-3">
            {race.country_flag && <img src={race.country_flag} alt="Flag" className="w-8 rounded-sm shadow-md" />}
            <span className="text-gray-400 text-sm font-mono">{race.date}</span>
          </div>
          {isNext && <span className="bg-oracle-red text-white text-[10px] font-bold px-2 py-1 rounded-full animate-pulse flex items-center gap-1 shadow-red-glow"><Cpu size={12} /> PREDICTION</span>}
          {isCancelled && <span className="bg-gray-800 text-gray-400 border border-gray-600 text-[10px] font-bold px-2 py-1 rounded-full flex items-center gap-1"><AlertTriangle size={12} /> CANCELLED</span>}
        </div>

        <h2 className="text-2xl font-bold text-white mb-2 uppercase tracking-tight">{race.name}</h2>
        <div className="flex items-center gap-2 text-oracle-red text-sm mb-1 font-medium"><MapPin size={14} /> {race.location}</div>
        {!isCancelled && <div className="flex items-center gap-2 text-gray-500 text-xs mb-6 font-mono"><Clock size={12} /> Local: <span className="text-gray-300">{localTime}</span></div>}

        {(isCompleted || isNext) && (
          <button onClick={() => setIsOpen(!isOpen)} className="mt-auto w-full py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg flex items-center justify-center gap-2 text-white font-medium transition-colors">
            {isOpen ? "Close View" : isNext ? "Open AI Prediction" : "Open Official Results"}
            <ChevronRight size={18} className={`transition-transform duration-300 ${isOpen ? "rotate-180 md:rotate-180 rotate-90" : ""}`} />
          </button>
        )}
      </div>

      {/* RIGHT PANE: Expanding Grid */}
      <div className={`flex-1 transition-opacity duration-500 delay-150 border-t md:border-t-0 md:border-l border-white/10 pt-6 md:pt-0 md:pl-6 ${isOpen ? "opacity-100" : "opacity-0 hidden"}`}>
        {/* MOBILE FIX: max-h-[400px] overflow-y-auto traps the scroll inside the card on cellphones! */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 h-full max-h-[400px] md:max-h-none overflow-y-auto md:overflow-visible pr-2 md:pr-0 custom-scrollbar">
          <div className="flex flex-col gap-3">{col1.map((d, i) => <DriverRow key={`col1-${i}`} driver={d} isNext={isNext} />)}</div>
          <div className="flex flex-col gap-3">{col2.map((d, i) => <DriverRow key={`col2-${i}`} driver={d} isNext={isNext} />)}</div>
          <div className="flex flex-col gap-3">{col3.map((d, i) => <DriverRow key={`col3-${i}`} driver={d} isNext={isNext} />)}</div>
        </div>
      </div>
    </div>
  );
}

// Sub-component rendering
function DriverRow({ driver, isNext }: { driver: DriverResult, isNext: boolean }) {
  const posColor = driver.position === 1 ? "text-yellow-400" :
                   driver.position === 2 ? "text-gray-300" :
                   driver.position === 3 ? "text-amber-600" :
                   driver.position === "DNF" ? "text-gray-600" : "text-oracle-red";

  const nameParts = driver.name.split(" ");
  const firstName = nameParts[0];
  const lastName = nameParts.slice(1).join(" ").toUpperCase(); 
  
  const searchName = driver.name.toUpperCase().trim(); 
  const teamColor = driverColors[searchName] || "#FFFFFF";

  return (
    <div className={`p-3 rounded-lg border flex flex-col gap-2 transition-colors ${isNext ? 'bg-black/60 border-oracle-red/20' : 'bg-transparent border-white/5 border-b-white/10'}`}>
      <div className="flex justify-between items-center">
        
        <div className="flex items-center gap-3">
          <span className={`font-bold w-6 text-lg ${posColor}`}>
            {driver.position === "DNF" ? "DNF" : `P${driver.position}`}
          </span>
          
          <div className="leading-none">
            <span className="text-gray-400 text-[10px] uppercase tracking-widest">{firstName}</span><br />
            <span className="font-bold text-sm tracking-tight drop-shadow-md" style={{ color: teamColor }}>
              {lastName}
            </span>
          </div>
        </div>

        {!isNext && (
          <span className="text-gray-500 font-mono text-xs text-right">
            {driver.position === "DNF" ? "OUT" : (driver.gap || "Winner")}
          </span>
        )}
      </div>
      
      {isNext && driver.explanation && (
        <p className="text-[11px] text-gray-400 leading-tight mt-1 border-t border-white/5 pt-2">
          {driver.explanation}
        </p>
      )}
    </div>
  );
}