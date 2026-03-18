"use client";

import RaceCarousel from "@/components/RaceCarousel";
import { Activity, Database, Cpu, User, Zap, Code2, LineChart, Instagram, Github, Linkedin, Globe } from "lucide-react";
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
          <h1 className="text-3xl md:text-3xl md:text-4xl font-bold tracking-tighter text-white flex items-center gap-3">
              <LineChart size={36} className="text-oracle-red drop-shadow-red-glow" />
              <span>GRID <span className="text-oracle-red drop-shadow-red-glow">ORACLE</span></span>
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
            <h2 className="text-3xl md:text-4xl font-bold text-white tracking-tight leading-tight">
              Gut feelings don't win championships. <br/>
              <span className="text-oracle-red">Data does.</span>
            </h2>
            <p className="text-gray-400 leading-relaxed text-lg">
              Can I be for real? This whole thing started because i was BORED. But I also wanted to see how further an AI could go with the same vision that we, spectators, have. "If I fed an AI all the data I have access to, could it predict the grid better than I can?" That was the question. And here we are. 
            </p>
            <p className="text-gray-400 leading-relaxed text-lg">
              The objective its very simple: The Oracle will drop a 22-Driver prediction on the previous race, based on the telemetry data for that weekend, along with the past performances too. Zero human touches, just like our future! Astonishing!! Ain't that cool?!?!?!
            </p>
          </div>
          <div className="flex-1 w-full bg-oracle-dark/50 border border-white/5 rounded-2xl p-8 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-64 h-64 bg-oracle-red/10 blur-[80px] group-hover:bg-oracle-red/20 transition-colors duration-700" />
            <LineChart size={180} strokeWidth={0.5} className="text-white/5 absolute -bottom-10 -left-10" />
            <div className="relative z-10 space-y-4 font-mono text-sm text-gray-500">
              <p className="text-oracle-red">{">"} STARTING PROCESS...</p>
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
            <h2 className="text-3xl md:text-4xl font-bold text-white tracking-tight leading-tight">
              OpenF1 meets <span className="text-oracle-red">Llama 3.3</span>
            </h2>
            <p className="text-gray-400 leading-relaxed text-lg">
              Different of the average F1 fans, every monday after a race, the Python script will look up at the data at <span className="text-white font-mono">OpenF1 API</span>. It pulls everything: session times, driver gaps, DNFs and more.
            </p>
            <p className="text-gray-400 leading-relaxed text-lg">
              Unfortunately, I did it all for free, and AI hates all that JSON yap and has limited tokens, so I resumed the past seasons (2023-2025) on a .txt, wich I sent to the amazing and lovely <span className="text-white font-mono">Llama-3.3-70b</span> model.
            </p>
            <p className="text-gray-400 leading-relaxed text-lg">
              With those two connected, everything its automatized and auto-filled every day after the race, dropping a different prediction for every next race!
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
          className="flex flex-col-reverse md:flex-row items-center gap-10 md:gap-12 bg-oracle-dark/30 border border-white/5 p-6 md:p-12 rounded-3xl relative overflow-hidden"
        >
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-oracle-red to-transparent opacity-50" />
          
          {/* Text Content - Centered on mobile, left-aligned on desktop */}
          <div className="flex-1 space-y-6 z-10 flex flex-col items-center md:items-start text-center md:text-left">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs text-gray-400 font-mono tracking-widest uppercase">
              <User size={14} className="text-oracle-red" /> The Dev
            </div>
            <h2 className="text-3xl md:text-4xl font-bold text-white tracking-tight leading-tight">
              Arthur Figueiredo<span className="text-gray-500 text-xl md:text-2xl font-normal block mt-1">Systems Analysis & Dev</span>
            </h2>
            <p className="text-gray-400 leading-relaxed text-base md:text-lg">
              I'm the guy who builds stuff like this instead of doing normal things on weekends. As the founder of <span className="text-white font-bold">Percorsi Co.</span>, I'm constantly looking for ways to mash up raw logic with great design.
            </p>
            <p className="text-gray-400 leading-relaxed text-base md:text-lg">
              <strong className="text-white">What's next for the Oracle?</strong> I'm working on a feedback loop between AI's, just like Real Steel, I wanna see them robots fighting themselves!! Basically, i want to improve the AI using another AI, wich tells where it failed, how many and by how much the AI got the predictions right. 
            </p>
            
            {/* Buttons - Stacked on mobile, side-by-side on larger screens */}
            <div className="pt-4 flex flex-col sm:flex-row items-center justify-center md:justify-start gap-4 w-full">
              <a href="https://instagram.com/arthur.script" target="_blank" rel="noopener noreferrer" className="flex items-center justify-center gap-2 px-5 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-white font-medium transition-all group w-full sm:w-auto">
                <span className="text-gray-400 group-hover:text-oracle-red transition-colors font-bold">@arthur.script</span>
              </a>
              <a href="https://github.com/guifigueireedo" target="_blank" rel="noopener noreferrer" className="flex items-center justify-center gap-2 px-5 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-white font-medium transition-all group w-full sm:w-auto">
                <span className="text-gray-400 group-hover:text-oracle-red transition-colors font-bold">GitHub</span>
              </a>
              <a href="https://linkedin.com/in/guifigueireedo" target="_blank" rel="noopener noreferrer" className="flex items-center justify-center gap-2 px-5 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-white font-medium transition-all group w-full sm:w-auto">
                <span className="text-gray-400 group-hover:text-oracle-red transition-colors font-bold">LinkedIn</span>
              </a>
              <a href="https://arthur-figueiredo.netlify.app" target="_blank" rel="noopener noreferrer" className="flex items-center justify-center gap-2 px-5 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-white font-medium transition-all group w-full sm:w-auto">
                <span className="text-gray-400 group-hover:text-oracle-red transition-colors font-bold">Portfolio</span>
              </a>
            </div>
          </div>
          
          {/* Image Container - Added shrink-0 to prevent oval squishing and margin to separate from text */}
          <div className="w-full md:w-1/3 flex justify-center z-10 mb-2 md:mb-0">
            <div className="w-48 h-48 md:w-64 md:h-64 shrink-0 rounded-full border-4 border-oracle-red/20 shadow-red-glow-intense flex items-center justify-center bg-oracle-dark relative overflow-hidden">
               <img src="/me.jpeg" alt="Arthur - Percorsi Co." className="w-full h-full object-cover" />
            </div>
          </div>
        </motion.div>
      </section>
    </main>
  );
}