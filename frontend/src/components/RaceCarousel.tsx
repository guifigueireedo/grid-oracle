// src/components/RaceCarousel.tsx
"use client";

import { useRef } from "react";
import { motion, useScroll } from "framer-motion";
import calendar from "../data/calendar.json";
import RaceCard from "./RaceCard"; 

// 1. Tell TypeScript exactly what the JSON data looks like
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
  status: "cancelled" | "completed" | "next" | "future";
  results?: DriverResult[];
  predictions?: DriverResult[];
}

// 2. Cast the imported JSON as an array of our defined RaceEvent type
const raceCalendar = calendar as RaceEvent[];

export default function RaceCarousel() {
  const targetRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: targetRef });

  return (
    <div ref={targetRef} className="w-full relative overflow-x-auto flex gap-6 px-6 pb-12 pt-4 snap-x snap-mandatory">
      {/* 3. Give 'race' and 'index' strict types inside the map function */}
      {raceCalendar.map((race: RaceEvent, index: number) => (
        <div key={race.id} className="snap-center shrink-0">
          <RaceCard race={race} />
        </div>
      ))}
    </div>
  );
}