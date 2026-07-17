import FrequencyBarChart from './FrequencyBarChart';

interface LiveCryptanalysisProps {
  ioc: number;
  frequencies: Record<string, number>;
}

export default function LiveCryptanalysis({ ioc, frequencies }: LiveCryptanalysisProps) {
  return (
    <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-sm flex flex-col space-y-6">
      <h2 className="text-lg font-bold text-slate-200 flex items-center">
        <svg className="w-5 h-5 mr-2 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 002 2h2a2 2 0 002-2z" />
        </svg>
        Live Cryptanalysis
      </h2>

      {/* Index of Coincidence Widget */}
      <div className="flex flex-col space-y-2">
        <div className="flex items-center justify-between text-sm">
          <span className="text-slate-400 font-semibold">Index of Coincidence (IC)</span>
          <span className="font-mono text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/25">
            {ioc.toFixed(5)}
          </span>
        </div>

        {/* Progress bar visualizer for IC */}
        <div className="w-full h-3 bg-slate-950 rounded-full relative overflow-hidden border border-slate-900">
          {/* Random text IC marker (0.0385) */}
          <div className="absolute left-[38.5%] top-0 w-0.5 h-full bg-slate-700 z-10" title="Random Text IC: 0.0385"></div>
          {/* English text IC marker (0.0667) */}
          <div className="absolute left-[66.7%] top-0 w-0.5 h-full bg-slate-700 z-10" title="English Text IC: 0.0667"></div>

          {/* Active value fill */}
          <div
            className={`h-full transition-all duration-500 rounded-full ${
              Math.abs(ioc - 0.0667) < 0.008
                ? 'bg-gradient-to-r from-emerald-500 to-emerald-600'
                : ioc > 0.08 ? 'bg-indigo-600' : 'bg-gradient-to-r from-amber-500 to-amber-600'
            }`}
            style={{ width: `${Math.min(ioc * 1000, 100)}%` }}
          ></div>
        </div>

        <div className="flex justify-between text-[9px] font-mono text-slate-500 px-1">
          <span>Random (0.0385)</span>
          <span className="text-slate-400 font-bold">English (0.0667)</span>
          <span>Monolithic (1.0)</span>
        </div>
      </div>

      {/* Live Frequency Distribution Comparison Bar chart */}
      <div className="flex flex-col space-y-3">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Letter Frequencies vs. Standard English</span>
        <FrequencyBarChart frequencies={frequencies} />
      </div>
    </div>
  );
}
