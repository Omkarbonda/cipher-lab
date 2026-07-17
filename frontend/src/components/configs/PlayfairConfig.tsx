interface PlayfairConfigProps {
  playfairKey: string;
  setPlayfairKey: (key: string) => void;
}

export default function PlayfairConfig({ playfairKey, setPlayfairKey }: PlayfairConfigProps) {
  return (
    <div className="flex flex-col space-y-3">
      <div className="flex flex-col space-y-1">
        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Playfair Key Seed Word</label>
        <input
          type="text"
          className="bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-sm text-slate-200 font-mono focus:outline-none focus:border-indigo-500/80 transition-colors"
          value={playfairKey}
          onChange={(e) => setPlayfairKey(e.target.value.toUpperCase().replace(/[^A-Z]/g, ''))}
          placeholder="e.g. KEYWORD"
        />
      </div>
      <span className="text-[10px] text-slate-500">
        The 5x5 Playfair grid is populated with this seed first (merging 'J' into 'I'), followed by the rest of the alphabet.
      </span>
    </div>
  );
}
