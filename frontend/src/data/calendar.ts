export type RaceStatus = 'cancelled' | 'completed' | 'next' | 'future';

export interface DriverResult {
  name: string;
  position: number | 'DNF';
  gap?: string;
  explanation?: string;
}

export interface RaceEvent {
  id: string;
  name: string;
  location: string;
  date: string;
  status: RaceStatus;
  results?: DriverResult[];
  predictions?: DriverResult[];
}

export const raceCalendar: RaceEvent[] = [
  {
    id: "bhr_2026",
    name: "Bahrain Grand Prix",
    location: "Sakhir",
    date: "Cancelled",
    status: "cancelled"
  },
  {
    id: "sau_2026",
    name: "Saudi Arabian Grand Prix",
    location: "Jeddah",
    date: "Cancelled",
    status: "cancelled"
  },
  {
    id: "aus_2026",
    name: "Australian Grand Prix",
    location: "Melbourne",
    date: "Mar 06 - 08, 2026",
    status: "completed",
    results: [
      { name: "Oscar PIASTRI", position: 1 },
      { name: "Kimi ANTONELLI", position: 2, gap: "+2.974s" },
      { name: "Charles LECLERC", position: 3, gap: "+15.519s" },
    ]
  },
  {
    id: "chn_2026",
    name: "Chinese Grand Prix",
    location: "Shanghai",
    date: "Mar 20 - 22, 2026",
    status: "completed",
    results: [
      { name: "Max VERSTAPPEN", position: 1 },
      { name: "Oscar PIASTRI", position: 2, gap: "+4.120s" },
      { name: "Lando NORRIS", position: 3, gap: "+6.800s" },
    ]
  },
  {
    id: "jpn_2026",
    name: "Japanese Grand Prix",
    location: "Suzuka",
    date: "Apr 03 - 05, 2026",
    status: "next",
    predictions: [
      { 
        name: "Max VERSTAPPEN", 
        position: 1, 
        explanation: "P1 - VERSTAPPEN (3) - High-speed mastery at Suzuka remains his strongest asset. Gaps from Australia indicate the RB21's aero efficiency is recovering." 
      },
      { 
        name: "Lando NORRIS", 
        position: 2, 
        explanation: "P2 - NORRIS (1) - The McLaren excels in sector 1 sweeps, but historical data shows slight vulnerability on tire deg here compared to Red Bull." 
      },
      { 
        name: "George RUSSELL", 
        position: 3, 
        explanation: "P3 - RUSSELL (63) - Consistently strong in high-speed permanent tracks, and the Mercedes shows great balance in the fast corners." 
      }
    ]
  },
  {
    id: "mia_2026",
    name: "Miami Grand Prix",
    location: "Miami",
    date: "May 01 - 03, 2026",
    status: "future"
  }
];