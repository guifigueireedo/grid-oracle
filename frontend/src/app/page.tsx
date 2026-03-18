"use client";

import RaceCarousel from "@/components/RaceCarousel";
import { Activity, Database, Cpu, User, ArrowRight, Github, Instagram, Zap, Code2, LineChart } from "lucide-react";
import { motion, Variants } from "framer-motion";

export default function Home() {
  // Animation variants for smooth scrolling reveals
  const fadeUp: Variants = {
    hidden: { opacity: 0, y: 40 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.8, ease: "easeOut" } }
  };

  return (
    <main className="min-h-screen bg-oracle-black flex flex-col pt-12 relative overflow-x-hidden">
      {/* Background ambient glow */}
      <div className="absolute top-0 left-[20%] w-[60%] h-[40%] bg-oracle-red blur-[150px] opacity-10 rounded-full pointer-events-none" />
      
      {/* Header */}
      <header className="container mx-auto px-6 mb-8 relative z-10 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold tracking-tighter text-white flex items-center gap-3">
            GRID <span className="text-oracle-red drop-shadow-red-glow">ORACLE</span>
          </h1>
          <p className="text-gray-400 mt-2 tracking-wide text-sm uppercase">2026 AI Strategy Predictor</p>
        </div>
        <div className="hidden md:flex items-center gap-2 text-oracle-red font-mono text-sm border border-oracle-red/30 bg-oracle-red/10 px-4 py-2 rounded-full shadow-red-glow">
          <Activity size={16} className="animate-pulse" />
          SYSTEM ONLINE
        </div>
      </header>

      {/* The Carousel */}
      <div className="w-full relative z-10 mb-32">
        <RaceCarousel />
      </div>

      {/* Narrative Sections */}
      <section className="container mx-auto px-6 pb-32 relative z-10 flex flex-col gap-32">
        
        {/* SECTION 1: THE ORIGIN */}
        <motion.div 
          initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-100px" }} variants={fadeUp}
          className="flex flex-col md:flex-row items-center gap-12"
        >
          <div className="flex-1 space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs text-gray-400 font-mono tracking-widest uppercase">
              <Zap size={14} className="text-oracle-red" /> The Objective
            </div>
            <h2 className="text-4xl font-bold text-white tracking-tight leading-tight">
              Gut feelings don't win championships. <br/>
              <span className="text-oracle-red">Data does.</span>
            </h2>
            <p className="text-gray-400 leading-relaxed text-lg">
              Can I be for real? This whole thing started because i was BORED. But I also wanted to see how further an AI could go with the same vision that we, spectators, have. "If I fed an AI all the data I have access to, could it predict the grid better than I can?" That was the question. And here we are. 
            </p>
            <p className="text-gray-400 leading-relaxed text-lg">
              The objective its very simple: Every Monday morning after a race, the Oracle will drop a 22-Driver prediction on the another race,
            </p>
          </div>
          <div className="flex-1 w-full bg-oracle-dark/50 border border-white/5 rounded-2xl p-8 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-64 h-64 bg-oracle-red/10 blur-[80px] group-hover:bg-oracle-red/20 transition-colors duration-700" />
            <LineChart size={180} strokeWidth={0.5} className="text-white/5 absolute -bottom-10 -left-10" />
            <div className="relative z-10 space-y-4 font-mono text-sm text-gray-500">
              <p className="text-oracle-red">{">"} INITIATING SEQUENCE...</p>
              <p>{">"} LOADING HISTORICAL RESUMES</p>
              <p>{">"} ANALYZING DRIVER PERFORMANCE</p>
              <p className="text-white animate-pulse">{">"} READY TO PREDICT</p>
            </div>
          </div>
        </motion.div>

        {/* SECTION 2: THE TECH */}
        <motion.div 
          initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-100px" }} variants={fadeUp}
          className="flex flex-col md:flex-row-reverse items-center gap-12"
        >
          <div className="flex-1 space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs text-gray-400 font-mono tracking-widest uppercase">
              <Database size={14} className="text-oracle-red" /> The Architecture
            </div>
            <h2 className="text-4xl font-bold text-white tracking-tight leading-tight">
              OpenF1 meets <span className="text-oracle-red">Llama 3.3</span>
            </h2>
            <p className="text-gray-400 leading-relaxed text-lg">
              We don't do magic 8-balls here. Every Monday, a custom Python script wakes up and hits the <span className="text-white font-mono">OpenF1 API</span>. It pulls everything: session times, driver gaps, DNFs, you name it.
            </p>
            <p className="text-gray-400 leading-relaxed text-lg">
              But here's the trick: AI models hate bloated JSON files. So, the script distills the telemetry into a highly compressed format, slaps it next to a 2025 historical performance file, and hands it to Groq's blazing-fast <span className="text-white font-mono">Llama-3.3-70b</span> model. The AI cross-references the data, generates a data-grounded 22-driver grid prediction, and dumps it right back into this Next.js frontend. Fully automated. 
            </p>
          </div>
          <div className="flex-1 w-full grid grid-cols-2 gap-4">
            <div className="bg-oracle-dark border border-white/5 p-6 rounded-2xl flex flex-col items-center justify-center text-center gap-3 hover:border-oracle-red/30 transition-all">
              <Code2 size={32} className="text-gray-400" />
              <span className="text-white font-bold">Next.js + Tailwind</span>
              <span className="text-xs text-gray-500 font-mono">The Chassis</span>
            </div>
            <div className="bg-oracle-dark border border-white/5 p-6 rounded-2xl flex flex-col items-center justify-center text-center gap-3 hover:border-oracle-red/30 transition-all">
              <Database size={32} className="text-gray-400" />
              <span className="text-white font-bold">OpenF1 API</span>
              <span className="text-xs text-gray-500 font-mono">The Fuel</span>
            </div>
            <div className="bg-oracle-dark border border-white/5 p-6 rounded-2xl flex flex-col items-center justify-center text-center gap-3 hover:border-oracle-red/30 transition-all">
              <Activity size={32} className="text-gray-400" />
              <span className="text-white font-bold">Python Scripts</span>
              <span className="text-xs text-gray-500 font-mono">The Engine</span>
            </div>
            <div className="bg-oracle-dark border border-oracle-red/30 p-6 rounded-2xl flex flex-col items-center justify-center text-center gap-3 shadow-[0_0_20px_rgba(255,30,30,0.1)] hover:shadow-red-glow transition-all">
              <Cpu size={32} className="text-oracle-red" />
              <span className="text-white font-bold">Llama-3.3-70b</span>
              <span className="text-xs text-oracle-red/70 font-mono">The Brain</span>
            </div>
          </div>
        </motion.div>

        {/* SECTION 3: THE DEVELOPER */}
        <motion.div 
          initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-100px" }} variants={fadeUp}
          className="flex flex-col md:flex-row items-center gap-12 bg-oracle-dark/30 border border-white/5 p-8 md:p-12 rounded-3xl relative overflow-hidden"
        >
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-oracle-red to-transparent opacity-50" />
          
          <div className="flex-1 space-y-6 z-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs text-gray-400 font-mono tracking-widest uppercase">
              <User size={14} className="text-oracle-red" /> The Dev
            </div>
            <h2 className="text-4xl font-bold text-white tracking-tight leading-tight">
              Arthur <span className="text-gray-500 text-2xl font-normal block mt-1">Systems Analysis & Dev</span>
            </h2>
            <p className="text-gray-400 leading-relaxed text-lg">
              I'm the guy who builds stuff like this instead of doing normal things on weekends. As the founder of <span className="text-white font-bold">Percorsi Co.</span>, I'm constantly looking for ways to mash up raw logic with great design.
            </p>
            <p className="text-gray-400 leading-relaxed text-lg">
              <strong className="text-white">What's next for the Oracle?</strong> I'm working on a feedback loop. Soon, the AI will grade its *own* past predictions against the real race results, figure out where it messed up (like underestimating Ferrari's tire deg), and automatically adjust its prompt for the next race. 
            </p>
            
            <div className="pt-4 flex items-center gap-4">
              <a href="https://instagram.com/arthur.script" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 px-5 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-white font-medium transition-all group">
                <Instagram size={18} className="text-gray-400 group-hover:text-oracle-red transition-colors" />
                @arthur.script
              </a>
              <a href="#" className="flex items-center gap-2 px-5 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-white font-medium transition-all group">
                <Github size={18} className="text-gray-400 group-hover:text-oracle-red transition-colors" />
                GitHub
              </a>
            </div>
          </div>
          
          <div className="w-full md:w-1/3 flex justify-center z-10">
            <div className="w-48 h-48 md:w-64 md:h-64 rounded-full border-4 border-oracle-red/20 shadow-red-glow-intense flex items-center justify-center bg-oracle-dark relative overflow-hidden">
               {}
               <User size={80} className="text-oracle-red opacity-50" />
            </div>
          </div>
        </motion.div>

      </section>
    </main>
  );
}