export default function CarouselSkeleton() {
  const skeletonCards = [1, 2, 3];

  return (
    <div className="w-full relative flex flex-col">
      <div className="flex items-center justify-end gap-3 mb-4 px-6 w-full">
        <div className="w-12 h-12 rounded-full bg-white/5 animate-pulse" />
        <div className="w-12 h-12 rounded-full bg-white/5 animate-pulse" />
      </div>

      <div className="w-full overflow-hidden flex gap-6 px-6 pb-8">
        {skeletonCards.map((index) => (
          <div 
            key={index} 
            className="w-[85vw] max-w-[380px] md:max-w-none md:w-[400px] shrink-0 min-h-[450px] bg-oracle-dark border border-white/5 rounded-xl p-6 relative flex flex-col overflow-hidden"
          >
            <div className="absolute top-0 left-[-100%] w-[50%] h-full bg-gradient-to-r from-transparent via-white/5 to-transparent skew-x-12 animate-[shimmer_2s_infinite]" />

            <div className="flex justify-between items-start mb-4">
              <div className="w-24 h-6 bg-white/10 rounded-md animate-pulse" />
              <div className="w-32 h-6 bg-oracle-red/20 rounded-full animate-pulse" />
            </div>

            <div className="w-3/4 h-8 bg-white/10 rounded-md mb-4 animate-pulse" />
            
            <div className="w-1/2 h-4 bg-white/5 rounded-md mb-2 animate-pulse" />
            <div className="w-2/3 h-4 bg-white/5 rounded-md mb-6 animate-pulse" />

            <div className="mt-auto w-full py-6 bg-white/5 rounded-lg animate-pulse border border-white/5" />
          </div>
        ))}
      </div>
    </div>
  );
}