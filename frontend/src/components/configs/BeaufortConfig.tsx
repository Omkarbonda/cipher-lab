interface BeaufortConfigProps {
  beaufortKey: string;
  setBeaufortKey: (key: string) => void;
}

export default function BeaufortConfig({ beaufortKey, setBeaufortKey }: BeaufortConfigProps) {
  return (
    <div className="flex flex-col space-y-3">
      <div className="flex flex-col space-y-1">
        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Beaufort Keyword</label>
        <input
          type="text"
          className="bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-sm text-slate-200 font-mono focus:outline-none focus:border-indigo-500/80 transition-colors"
          value={beaufortKey}
          onChange={(e) => setBeaufortKey(e.target.value.toUpperCase().replace(/[^A-Z]/g, ''))}
          placeholder="e.g. KEYWORD"
        />
      </div>
      <span className="text-[10px] text-slate-500">
        Beaufort cipher is reciprocal: encryption and decryption use the same operation. The key determines the substitution mapping.
      </span>
    </div>
  );
}
