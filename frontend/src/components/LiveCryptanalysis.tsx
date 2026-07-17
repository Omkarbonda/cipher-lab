import FrequencyBarChart from './FrequencyBarChart';

interface LiveCryptanalysisProps {
  ioc: number;
  frequencies: Record<string, number>;
}

export default function LiveCryptanalysis({ ioc, frequencies }: LiveCryptanalysisProps) {
  return (
    <div className="border border-ink-500 bg-ink-700/60">
      {/* Panel header */}
      <div className="flex items-center justify-between px-4 py-2 bg-ink-600/80 border-b border-ink-500">
        <span className="text-[10px] text-parchment/40 tracking-[0.2em] uppercase">Live Cryptanalysis</span>
        <span className="text-[9px] text-amber/50 tracking-[0.15em] uppercase flex items-center gap-1.5">
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full rounded-full bg-amber opacity-50 animate-ping" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-amber" />
          </span>
          Monitoring
        </span>
      </div>

      <div className="p-4 flex flex-col space-y-5">
        {/* Index of Coincidence — amber gauge style */}
        <div className="flex flex-col space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[11px] text-parchment/60 tracking-[0.1em] uppercase">Index of Coincidence</span>
            <span className="font-mono text-sm text-brass bg-brass/8 border border-brass/20 px-2 py-0.5">
              {ioc.toFixed(5)}
            </span>
          </div>

          {/* IC Gauge */}
          <div className="w-full h-2 bg-ink-900 relative overflow-hidden border border-ink-500">
            {/* Random text marker */}
            <div className="absolute left-[38.5%] top-0 w-px h-full bg-parchment/10" />
            {/* English text marker */}
            <div className="absolute left-[66.7%] top-0 w-px h-full bg-parchment/20" />
            {/* Active fill */}
            <div
              className={`h-full transition-all duration-500 ${
                Math.abs(ioc - 0.0667) < 0.008
                  ? 'bg-brass'
                  : ioc > 0.08
                  ? 'bg-amber/70'
                  : 'bg-amber/50'
              }`}
              style={{ width: `${Math.min(ioc * 1000, 100)}%` }}
            />
          </div>

          <div className="flex justify-between text-[8px] font-mono text-parchment/25 tracking-[0.05em]">
            <span>Random (0.0385)</span>
            <span className="text-parchment/40">English (0.0667)</span>
            <span>Mono (1.0)</span>
          </div>
        </div>

        {/* Frequency chart */}
        <div className="flex flex-col space-y-2">
          <span className="text-[10px] text-parchment/40 tracking-[0.2em] uppercase">Letter Frequencies vs English</span>
          <FrequencyBarChart frequencies={frequencies} />
        </div>
      </div>
    </div>
  );
}
