"use client";

import { ChevronRight, Trophy, AlertTriangle, Cpu, MapPin, Clock } from "lucide-react";
import { useState, useEffect } from "react";

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

interface RaceCardProps {
  race: RaceEvent;
}

export default function RaceCard({ race }: RaceCardProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [localTime, setLocalTime] = useState<string>("Calculating...");

  useEffect(() => {
    if (race.date_start_utc) {
      const date = new Date(race.date_start_utc);
      const timeString = new Intl.DateTimeFormat('en-US', {
        weekday: 'short',
        hour: 'numeric',
        minute: '2-digit',
        timeZoneName: 'short'
      }).format(date);
      setLocalTime(timeString);
    } else {
      setLocalTime("TBA");
    }
  }, [race.date_start_utc]);

  const isNext = race.status === "next";
  const isCompleted = race.status === "completed";
  const isCancelled = race.status === "cancelled";

  // The 8-8-6 Column Splitter Function
  const displayData = isNext ? race.predictions : race.results;
  const col1 = displayData?.slice(0, 8) || [];
  const col2 = displayData?.slice(8, 16) || [];
  const col3 = displayData?.slice(16) || [];

  return (
    <div 
      // The magic happens here: width transitions from 400px to 1200px (on desktop)
      className={`transition-all duration-500 ease-in-out bg-oracle-dark border rounded-xl p-6 relative flex flex-col md:flex-row gap-6 overflow-hidden group snap-start
        ${isOpen ? "w-[320px] md:w-[1100px]" : "w-[320px] md:w-[400px]"}
        ${isNext ? "border-oracle-red shadow-red-glow" : "border-white/5"}
        ${isCancelled ? "opacity-50 grayscale" : ""}
      `}
    >
      {/* LEFT PANE: Original Card Content (Fixed Width) */}
      <div className="w-full md:w-[352px] shrink-0 flex flex-col min-h-[450px] relative z-10">
        
        {/* Background Circuit Image */}
        {race.circuit_image && (
          <div className="absolute top-10 -right-10 w-48 opacity-10 pointer-events-none transition-transform duration-500 group-hover:scale-110">
            <img src={race.circuit_image} alt="Circuit Layout" className="w-full h-full object-contain filter invert" />
          </div>
        )}

        {/* Top Section */}
        <div className="flex justify-between items-start mb-4">
          <div className="flex items-center gap-3">
            {race.country_flag && <img src={race.country_flag} alt="Flag" className="w-8 rounded-sm shadow-md" />}
            <span className="text-gray-400 text-sm font-mono">{race.date}</span>
          </div>
          {isNext && (
            <span className="bg-oracle-red text-white text-[10px] font-bold px-2 py-1 rounded-full animate-pulse flex items-center gap-1 shadow-red-glow">
              <Cpu size={12} /> PREDICTION READY
            </span>
          )}
          {isCancelled && (
            <span className="bg-gray-800 text-gray-400 border border-gray-600 text-[10px] font-bold px-2 py-1 rounded-full flex items-center gap-1">
              <AlertTriangle size={12} /> CANCELLED
            </span>
          )}
        </div>

        {/* Main Info */}
        <h2 className="text-2xl font-bold text-white mb-2 uppercase tracking-tight">{race.name}</h2>
        <div className="flex items-center gap-2 text-oracle-red text-sm mb-1 font-medium">
          <MapPin size={14} /> {race.location}
        </div>
        {!isCancelled && (
          <div className="flex items-center gap-2 text-gray-500 text-xs mb-6 font-mono">
            <Clock size={12} /> Local: <span className="text-gray-300">{localTime}</span>
          </div>
        )}

        {/* The "Dropright" Toggle Button */}
        {(isCompleted || isNext) && (
          <button 
            onClick={() => setIsOpen(!isOpen)}
            className="mt-auto w-full py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg flex items-center justify-center gap-2 text-white font-medium transition-colors"
          >
            {isOpen ? "Close View" : isNext ? "Open AI Prediction" : "Open Official Results"}
            <ChevronRight size={18} className={`transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`} />
          </button>
        )}
      </div>

      {/* RIGHT PANE: The 3-Column Expanded Grid */}
      <div 
        className={`flex-1 transition-opacity duration-500 delay-150 border-t md:border-t-0 md:border-l border-white/10 pt-6 md:pt-0 md:pl-6
          ${isOpen ? "opacity-100" : "opacity-0 hidden"}
        `}
      >
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 h-full">
          {/* Column 1 (8 Drivers) */}
          <div className="flex flex-col gap-3">
            {col1.map((d, i) => <DriverRow key={i} driver={d} isNext={isNext} />)}
          </div>
          {/* Column 2 (8 Drivers) */}
          <div className="flex flex-col gap-3">
            {col2.map((d, i) => <DriverRow key={i} driver={d} isNext={isNext} />)}
          </div>
          {/* Column 3 (6 Drivers) */}
          <div className="flex flex-col gap-3">
            {col3.map((d, i) => <DriverRow key={i} driver={d} isNext={isNext} />)}
          </div>
        </div>
      </div>
    </div>
  );
}

// Sub-component to render each driver row cleanly
function DriverRow({ driver, isNext }: { driver: DriverResult, isNext: boolean }) {
  const isPodium = driver.position === 1 || driver.position === 2 || driver.position === 3;
  
  return (
    <div className={`p-3 rounded-lg border flex flex-col gap-1 transition-colors ${isNext ? 'bg-black/60 border-oracle-red/20' : 'bg-transparent border-white/5 border-b-white/10'}`}>
      <div className="flex justify-between items-center">
        <span className="text-gray-200 text-sm font-bold flex items-center gap-2">
          {isNext && isPodium && <Trophy size={12} className={driver.position === 1 ? "text-yellow-500" : driver.position === 2 ? "text-gray-300" : "text-orange-400"} />}
          <span className={driver.position === 'DNF' ? 'text-gray-500' : 'text-oracle-red'}>
            {driver.position === "DNF" ? "DNF" : `P${driver.position}`}
          </span>
          {driver.name}
        </span>
        {!isNext && <span className="text-gray-500 font-mono text-xs">{driver.gap || "Winner"}</span>}
      </div>
      {isNext && driver.explanation && (
        <p className="text-[11px] text-gray-400 leading-tight mt-1">{driver.explanation}</p>
      )}
    </div>
  );
}