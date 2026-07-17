interface SubstitutionConfigProps {
  substitutionKey: string;
  setSubstitutionKey: (key: string) => void;
  generateRandomSubstitutionKey: () => void;
}

export default function SubstitutionConfig({
  substitutionKey,
  setSubstitutionKey,
  generateRandomSubstitutionKey,
}: SubstitutionConfigProps) {
  return (
    <div className="flex flex-col space-y-4">
      <div className="flex flex-col space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Substitution Alphabet Map</label>
          <button
            onClick={generateRandomSubstitutionKey}
            className="text-[10px] text-indigo-400 hover:text-indigo-300 font-bold uppercase"
          >
            🎲 Randomize Map
          </button>
        </div>

        <input
          type="text"
          maxLength={26}
          className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 font-mono tracking-[0.2em] uppercase focus:outline-none focus:border-indigo-500/80 transition-colors"
          value={substitutionKey}
          onChange={(e) => setSubstitutionKey(e.target.value.toUpperCase())}
        />
      </div>

      {/* Character visual map */}
      <div className="flex flex-wrap gap-1.5 justify-center text-center font-mono text-[9px] text-slate-400 border border-slate-900 rounded bg-slate-950 p-2">
        {'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map((char, idx) => (
          <div key={char} className="flex flex-col px-1.5 py-0.5 bg-slate-900/50 rounded border border-slate-850 min-w-[28px]">
            <span className="text-slate-600 font-bold border-b border-slate-900/60 pb-0.5">{char}</span>
            <span className="text-indigo-400 pt-0.5 font-bold">{substitutionKey[idx] || '?'}</span>
          </div>
        ))}
      </div>

      {substitutionKey.length !== 26 && (
        <span className="text-[10px] text-rose-400 font-medium">
          ⚠️ Key must be exactly 26 unique characters. Currently: {substitutionKey.length}
        </span>
      )}
    </div>
  );
}
