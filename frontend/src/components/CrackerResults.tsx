import type { CipherType, CrackCandidate } from '../types/cipher';

interface CrackerResultsProps {
  activeTab: CipherType;
  crackCandidates: CrackCandidate[];
  crackVigenereCandidates: CrackCandidate[];
  setCaesarShift: (shift: number) => void;
  setVigenereKey: (key: string) => void;
  setOutputText: (text: string) => void;
}

export default function CrackerResults({
  activeTab,
  crackCandidates,
  crackVigenereCandidates,
  setCaesarShift,
  setVigenereKey,
  setOutputText,
}: CrackerResultsProps) {
  const showCaesar = activeTab === 'caesar' && crackCandidates.length > 0;
  const showVigenere = activeTab === 'vigenere' && crackVigenereCandidates.length > 0;

  if (!showCaesar && !showVigenere) {
    return null;
  }

  return (
    <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-sm flex flex-col space-y-4 animate-fadeIn">
      <h2 className="text-lg font-bold text-slate-200 flex items-center justify-between">
        <span className="flex items-center">
          <svg className="w-5 h-5 mr-2 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Cracker Output Candidates
        </span>
        <span className="text-[10px] text-slate-400 font-normal">Sorted by best fitness</span>
      </h2>

      {/* Caesar Candidates list */}
      {activeTab === 'caesar' && (
        <div className="flex flex-col space-y-2.5">
          {crackCandidates.map((c, idx) => (
            <div
              key={c.shift}
              onClick={() => {
                setCaesarShift(c.shift!);
                setOutputText(c.plaintext);
              }}
              className={`flex flex-col space-y-1.5 p-3 rounded-xl border transition-all cursor-pointer text-left ${
                idx === 0
                  ? 'bg-indigo-500/10 border-indigo-500/35 hover:bg-indigo-500/15'
                  : 'bg-slate-950/40 border-slate-850 hover:bg-slate-900/40'
              }`}
            >
              <div className="flex items-center justify-between text-xs font-semibold">
                <span className="text-slate-200">Shift Key: {c.shift} {idx === 0 && '👑 (Best Guess)'}</span>
                <span className="font-mono text-slate-400">Score: {c.score} | Chi2: {c.chi2}</span>
              </div>
              <p className="text-xs text-indigo-300 font-mono truncate">
                {c.plaintext}
              </p>
            </div>
          ))}
        </div>
      )}

      {/* Vigenere Candidates list */}
      {activeTab === 'vigenere' && (
        <div className="flex flex-col space-y-2.5">
          {crackVigenereCandidates.map((c, idx) => (
            <div
              key={c.key}
              onClick={() => {
                setVigenereKey(c.key!);
                setOutputText(c.plaintext);
              }}
              className={`flex flex-col space-y-1.5 p-3 rounded-xl border transition-all cursor-pointer text-left ${
                idx === 0
                  ? 'bg-indigo-500/10 border-indigo-500/35 hover:bg-indigo-500/15'
                  : 'bg-slate-950/40 border-slate-850 hover:bg-slate-900/40'
              }`}
            >
              <div className="flex items-center justify-between text-xs font-semibold">
                <span className="text-slate-200">Key: {c.key} (Len: {c.key_length}) {idx === 0 && '👑 (Best Guess)'}</span>
                <span className="font-mono text-slate-400">Fitness: {c.score}</span>
              </div>
              <p className="text-xs text-indigo-300 font-mono truncate">
                {c.plaintext}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
