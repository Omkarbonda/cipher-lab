import { ENGLISH_FREQ } from '../types/cipher';

interface FrequencyBarChartProps {
  frequencies: Record<string, number>;
}

export default function FrequencyBarChart({ frequencies }: FrequencyBarChartProps) {
  const hasData = Object.keys(frequencies).length > 0;

  return (
    <div className="overflow-x-auto">
      <div className="h-40 flex items-end justify-between gap-[2px] bg-ink-900 border border-ink-500 p-3 relative min-w-[480px]">
        {!hasData && (
          <div className="absolute inset-0 flex items-center justify-center text-[10px] text-ink-400 italic tracking-[0.1em]">
            Type text to visualise frequencies
          </div>
        )}

        {'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map((char) => {
          const actualFreq = frequencies[char] || 0;
          const expectedFreq = ENGLISH_FREQ[char] || 0;
          const maxBound = 0.15;
          const actualHeight = Math.min((actualFreq / maxBound) * 100, 100);
          const expectedHeight = Math.min((expectedFreq / maxBound) * 100, 100);

          return (
            <div key={char} className="flex-1 flex flex-col items-center h-full group relative">
              {/* Tooltip */}
              <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 hidden group-hover:flex flex-col items-center pointer-events-none z-30">
                <div className="bg-ink-600 text-[8px] px-2 py-1 border border-ink-500 whitespace-nowrap text-left font-mono">
                  <div className="text-brass font-bold text-center border-b border-ink-500 pb-0.5 mb-0.5">{char}</div>
                  <div className="text-parchment/60">Actual: {(actualFreq * 100).toFixed(2)}%</div>
                  <div className="text-parchment/40">English: {(expectedFreq * 100).toFixed(2)}%</div>
                </div>
              </div>

              {/* Bars */}
              <div className="w-full flex-grow flex items-end justify-center relative">
                {/* English expected outline */}
                <div
                  className="absolute w-full border border-parchment/8 bg-parchment/5 rounded-t-[1px] pointer-events-none"
                  style={{ height: `${expectedHeight}%` }}
                />
                {/* Actual frequency bar */}
                <div
                  className={`w-full rounded-t-[1px] transition-all duration-300 z-10 ${
                    Math.abs(actualFreq - expectedFreq) < 0.015
                      ? 'bg-brass/70 group-hover:bg-brass/90'
                      : 'bg-amber/50 group-hover:bg-amber/70'
                  }`}
                  style={{ height: `${actualHeight}%` }}
                />
              </div>

              <span className="text-[7px] font-mono text-parchment/30 mt-1.5">{char}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
