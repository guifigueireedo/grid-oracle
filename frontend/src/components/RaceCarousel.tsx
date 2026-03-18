"use client";

import { useRef } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import calendar from "../data/calendar.json";
import RaceCard from "./RaceCard"; 

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

const raceCalendar = calendar as RaceEvent[];

export default function RaceCarousel() {
  const targetRef = useRef<HTMLDivElement>(null);

  const scroll = (direction: "left" | "right") => {
    if (targetRef.current) {
      const scrollAmount = direction === "left" ? -350 : 350;
      targetRef.current.scrollBy({ left: scrollAmount, behavior: "smooth" });
    }
  };

  return (
    <div className="w-full relative flex flex-col">
      <div className="flex items-center justify-end gap-3 mb-4 px-6 w-full">
        <button 
          onClick={() => scroll("left")} 
          className="p-3 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 hover:border-oracle-red transition-all group"
        >
          <ChevronLeft className="text-gray-400 group-hover:text-oracle-red transition-colors" />
        </button>
        <button 
          onClick={() => scroll("right")} 
          className="p-3 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 hover:border-oracle-red transition-all group"
        >
          <ChevronRight className="text-gray-400 group-hover:text-oracle-red transition-colors" />
        </button>
      </div>

      <div 
        ref={targetRef} 
        className="w-full overflow-x-auto flex gap-6 px-6 pb-8 snap-x snap-mandatory"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }} 
      >
        {raceCalendar.map((race: RaceEvent) => (
          <div key={race.id} className="snap-center shrink-0">
            <RaceCard race={race} />
          </div>
        ))}
      </div>
    </div>
  );
}