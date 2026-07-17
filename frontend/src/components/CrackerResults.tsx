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
    <div className="border border-ink-500 bg-ink-700/60 animate-fade-in">
      {/* Panel header */}
      <div className="flex items-center justify-between px-4 py-2 bg-ink-600/80 border-b border-ink-500">
        <span className="text-[10px] text-parchment/40 tracking-[0.2em] uppercase">Crack Candidates</span>
        <span className="text-[9px] text-parchment/30 tracking-[0.15em] uppercase">Best fit first</span>
      </div>

      <div className="p-3 flex flex-col space-y-2">
        {activeTab === 'caesar' && crackCandidates.map((c, idx) => (
          <div
            key={c.shift}
            onClick={() => {
              setCaesarShift(c.shift!);
              setOutputText(c.plaintext);
            }}
            className={`flex flex-col space-y-1 p-3 border cursor-pointer transition-all text-left ${
              idx === 0
                ? 'bg-amber/8 border-amber/25 hover:bg-amber/12'
                : 'bg-ink-800/40 border-ink-500 hover:bg-ink-700'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-semibold text-parchment/80 tracking-[0.05em]">
                Shift {c.shift}{idx === 0 && ' — best'}
              </span>
              <span className="font-mono text-[9px] text-parchment/30">
                χ² {c.chi2}
              </span>
            </div>
            <p className="text-[11px] text-brass/70 font-mono truncate leading-relaxed">
              {c.plaintext}
            </p>
          </div>
        ))}

        {activeTab === 'vigenere' && crackVigenereCandidates.map((c, idx) => (
          <div
            key={c.key}
            onClick={() => {
              setVigenereKey(c.key!);
              setOutputText(c.plaintext);
            }}
            className={`flex flex-col space-y-1 p-3 border cursor-pointer transition-all text-left ${
              idx === 0
                ? 'bg-amber/8 border-amber/25 hover:bg-amber/12'
                : 'bg-ink-800/40 border-ink-500 hover:bg-ink-700'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-semibold text-parchment/80 tracking-[0.05em]">
                Key: {c.key}{idx === 0 && ' — best'}
              </span>
              <span className="font-mono text-[9px] text-parchment/30">
                fit: {c.score}
              </span>
            </div>
            <p className="text-[11px] text-brass/70 font-mono truncate leading-relaxed">
              {c.plaintext}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
