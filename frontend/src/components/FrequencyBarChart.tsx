import { ENGLISH_FREQ } from '../types/cipher';

interface FrequencyBarChartProps {
  frequencies: Record<string, number>;
}

export default function FrequencyBarChart({ frequencies }: FrequencyBarChartProps) {
  const hasData = Object.keys(frequencies).length > 0;

  if (!hasData) {
    return (
      <div className="h-44 flex items-end justify-between gap-[3px] bg-slate-950 border border-slate-900 rounded-xl p-4 overflow-hidden relative">
        <div className="absolute inset-0 flex items-center justify-center text-xs text-slate-600 italic">
          Type text to visualize letter frequencies
        </div>
      </div>
    );
  }

  return (
    <div className="scrollable-chart">
      <div className="h-44 flex items-end justify-between gap-[3px] bg-slate-950 border border-slate-900 rounded-xl p-4 overflow-hidden relative min-w-[520px]">
      {'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map((char) => {
        const actualFreq = frequencies[char] || 0;
        const expectedFreq = ENGLISH_FREQ[char] || 0;

        const maxBound = 0.15;
        const actualHeight = Math.min((actualFreq / maxBound) * 100, 100);
        const expectedHeight = Math.min((expectedFreq / maxBound) * 100, 100);

        return (
          <div key={char} className="flex-1 flex flex-col items-center h-full group relative">
            {/* Interactive tooltip */}
            <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 hidden group-hover:flex flex-col items-center pointer-events-none z-30">
              <div className="bg-slate-900 text-[9px] px-2 py-1 rounded border border-slate-800 shadow-xl whitespace-nowrap text-left font-mono">
                <div className="text-slate-400 font-bold text-center border-b border-slate-800 pb-0.5 mb-0.5">{char}</div>
                <div>Actual: {(actualFreq * 100).toFixed(2)}%</div>
                <div>English: {(expectedFreq * 100).toFixed(2)}%</div>
              </div>
              <div className="w-1.5 h-1.5 bg-slate-900 rotate-45 -mt-[4px] border-r border-b border-slate-800"></div>
            </div>

            {/* Chart columns */}
            <div className="w-full flex-grow flex items-end justify-center relative">
              {/* English frequency target outline */}
              <div
                className="absolute w-full border border-slate-800 bg-slate-800/10 rounded-t-[1px] pointer-events-none"
                style={{ height: `${expectedHeight}%` }}
              ></div>
              {/* Actual frequency filled bar */}
              <div
                className={`w-full rounded-t-[1px] transition-all duration-300 z-10 ${
                  Math.abs(actualFreq - expectedFreq) < 0.015 ? 'bg-indigo-500/85 hover:bg-indigo-400' : 'bg-violet-600/70 hover:bg-violet-500'
                }`}
                style={{ height: `${actualHeight}%` }}
              ></div>
            </div>

            <span className="text-[8px] font-mono font-bold text-slate-600 mt-2">{char}</span>
          </div>
        );
      })}
    </div>
    </div>
  );
}
