"use client";

import { ChevronRight, Trophy, AlertTriangle, Cpu, MapPin, Clock } from "lucide-react";
import { useState, useEffect } from "react";
import Image from "next/image";

import driversBase from "../data/drivers.json";

interface DriverBase {
  name: string;
  driver_number: number;
  team_name: string;
  team_colour: string;
  headshot_url: string;
}

const driverMap = driversBase.reduce((acc, driver) => {
  acc[driver.name.toLowerCase()] = driver;
  return acc;
}, {} as Record<string, DriverBase>);

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
  
  const [expandedDriver, setExpandedDriver] = useState<string | null>(null);

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
  const col1 = displayData?.slice(0, 6) || [];
  const col2 = displayData?.slice(6, 12) || [];
  const col3 = displayData?.slice(12, 18) || [];
  const col4 = displayData?.slice(18) || [];

  return (
    <div 
      className={`transition-all duration-500 ease-in-out bg-oracle-dark border rounded-xl p-6 relative flex flex-col md:flex-row gap-6 overflow-hidden group snap-start
        ${isOpen ? "w-[85vw] max-w-[380px] md:max-w-none md:w-[1400px]" : "w-[85vw] max-w-[380px] md:max-w-none md:w-[400px]"}
        ${isNext ? "border-oracle-red shadow-red-glow" : "border-white/5"}
        ${isCancelled ? "opacity-50 grayscale" : ""}
      `}
    >
      <div className="w-full md:w-[352px] shrink-0 flex flex-col min-h-[450px] relative z-10">
        {(() => {
          const circuitImg = race.name.includes("Spanish") || race.location.includes("Barcelona") 
            ? "https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Spain%20carbon.png" 
            : race.circuit_image;

          return circuitImg ? (
            <div className="absolute top-10 -right-10 w-48 h-48 opacity-10 pointer-events-none transition-transform duration-500 group-hover:scale-110">
              <Image src={circuitImg} alt="Circuit Layout" fill className="object-contain filter invert" sizes="(max-width: 768px) 100vw, 200px" />
            </div>
          ) : null;
        })()}

        <div className="flex justify-between items-start mb-4 relative z-10">
          <div className="flex items-center gap-3">
            {race.country_flag && <Image src={race.country_flag} alt="Flag" width={32} height={20} className="rounded-sm shadow-md"/>}
            <span className="text-gray-400 text-sm font-mono">{race.date}</span>
          </div>
          {isNext && <span className="bg-oracle-red text-white text-[10px] font-bold px-2 py-1 rounded-full animate-pulse flex items-center gap-1 shadow-red-glow"><Cpu size={12} /> PREDICTION</span>}
          {isCancelled && <span className="bg-gray-800 text-gray-400 border border-gray-600 text-[10px] font-bold px-2 py-1 rounded-full flex items-center gap-1"><AlertTriangle size={12} /> CANCELLED</span>}
        </div>

        <h2 className="text-2xl font-bold text-white mb-2 uppercase tracking-tight relative z-10">{race.name}</h2>
        <div className="flex items-center gap-2 text-oracle-red text-sm mb-1 font-medium relative z-10"><MapPin size={14} /> {race.location}</div>
        {!isCancelled && <div className="flex items-center gap-2 text-gray-500 text-xs mb-6 font-mono relative z-10"><Clock size={12} /> Local: <span className="text-gray-300">{localTime}</span></div>}

        {(isCompleted || isNext) && (
          <button onClick={() => setIsOpen(!isOpen)} className="mt-auto w-full py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg flex items-center justify-center gap-2 text-white font-medium transition-colors relative z-10">
            {isOpen ? "Close View" : isNext ? "Open AI Prediction" : "Open Official Results"}
            <ChevronRight size={18} className={`transition-transform duration-300 ${isOpen ? "rotate-180 md:rotate-180 rotate-90" : ""}`} />
          </button>
        )}
      </div>

      <div className={`flex-1 transition-opacity duration-500 delay-150 border-t md:border-t-0 md:border-l border-white/10 pt-6 md:pt-0 md:pl-6 ${isOpen ? "opacity-100" : "opacity-0 hidden"}`}>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 h-full max-h-[400px] md:max-h-none overflow-y-auto md:overflow-visible pr-2 md:pr-0 custom-scrollbar">
          <div className="flex flex-col gap-3">{col1.map((d, i) => <DriverRow key={`col1-${i}`} driver={d} isNext={isNext} expandedDriver={expandedDriver} setExpandedDriver={setExpandedDriver} />)}</div>
          <div className="flex flex-col gap-3">{col2.map((d, i) => <DriverRow key={`col2-${i}`} driver={d} isNext={isNext} expandedDriver={expandedDriver} setExpandedDriver={setExpandedDriver} />)}</div>
          <div className="flex flex-col gap-3">{col3.map((d, i) => <DriverRow key={`col3-${i}`} driver={d} isNext={isNext} expandedDriver={expandedDriver} setExpandedDriver={setExpandedDriver} />)}</div>
          <div className="flex flex-col gap-3">{col4.map((d, i) => <DriverRow key={`col4-${i}`} driver={d} isNext={isNext} expandedDriver={expandedDriver} setExpandedDriver={setExpandedDriver} />)}</div>
        </div>
      </div>
    </div>
  );
}

function DriverRow({ 
  driver, 
  isNext, 
  expandedDriver, 
  setExpandedDriver 
}: { 
  driver: DriverResult, 
  isNext: boolean,
  expandedDriver: string | null,
  setExpandedDriver: (name: string | null) => void
}) {
  
  const isExpanded = expandedDriver === driver.name;

  const posColor = driver.position === 1 ? "text-yellow-400" :
                   driver.position === 2 ? "text-gray-300" :
                   driver.position === 3 ? "text-amber-600" :
                   driver.position === "DNF" ? "text-gray-600" : "text-oracle-red";

  const nameParts = driver.name.split(" ");
  const firstName = nameParts[0];
  const lastName = nameParts.slice(1).join(" "); 
  
  const baseData = driverMap[driver.name.toLowerCase()] || {};
  const teamColor = baseData.team_colour ? `#${baseData.team_colour}` : "#FFFFFF";
  const teamName = baseData.team_name || "Unknown Team";
  
  const logoFileName = teamName.toLowerCase().replace(/\s+/g, "_");
  const logoUrl = `/logos/${logoFileName}.png`;

  return (
    <div 
      onClick={() => setExpandedDriver(isExpanded ? null : driver.name)}
      className={`p-3 rounded-lg border flex flex-col gap-2 transition-all cursor-pointer group ${isNext ? 'bg-black/60 border-oracle-red/20 hover:border-oracle-red/50' : 'bg-transparent border-white/5 border-b-white/10 hover:bg-white/5'}`}
    >
      <div className="flex justify-between items-center">
        <div className={`flex items-center ${driver.position === "DNF" ? "gap-6" : driver.position <= 9 ? "gap-3" : "gap-5"}`}>
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
      
      {isExpanded && (
        <div className="mt-2 pt-3 border-t border-white/10 flex flex-col gap-3 animate-in fade-in slide-in-from-top-2 duration-300">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <div 
                      className="w-12 h-12 rounded-full border-2 overflow-hidden flex items-center justify-center bg-black/50 shrink-0" 
                      style={{ borderColor: teamColor }}
                    >
                        {baseData.headshot_url ? (
                            <img src={baseData.headshot_url} alt={driver.name} className="w-full h-full object-cover scale-110 mt-2" />
                        ) : (
                            <span className="text-gray-500 text-[10px] font-mono">N/A</span>
                        )}
                    </div>
                    <div>
                        <div className="flex items-center gap-2">
                           <span className="font-black text-xl italic" style={{ color: teamColor }}>
                             {baseData.driver_number || "00"}
                           </span>
                           <span className="text-white font-bold text-sm uppercase tracking-wide drop-shadow-md">
                             {teamName}
                           </span>
                        </div>
                    </div>
                </div>
                
                <div className="w-8 h-8 opacity-70">
                    <img src={logoUrl} alt={teamName} className="w-full h-full object-contain filter grayscale group-hover:grayscale-0 transition-all" onError={(e) => e.currentTarget.style.display = 'none'} />
                </div>
            </div>
            
            {isNext && driver.explanation && (
                <p className="text-[12px] text-gray-300 leading-relaxed bg-black/40 p-2.5 rounded-md border border-white/5 mt-1">
                    {driver.explanation}
                </p>
            )}
        </div>
      )}
    </div>
  );
}