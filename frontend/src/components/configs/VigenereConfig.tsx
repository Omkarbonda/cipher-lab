interface VigenereConfigProps {
  vigenereKey: string;
  setVigenereKey: (key: string) => void;
}

export default function VigenereConfig({ vigenereKey, setVigenereKey }: VigenereConfigProps) {
  return (
    <div className="flex flex-col space-y-3">
      <div className="flex flex-col space-y-1">
        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Repeating Keyword</label>
        <input
          type="text"
          className="bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-sm text-slate-200 font-mono focus:outline-none focus:border-indigo-500/80 transition-colors"
          value={vigenereKey}
          onChange={(e) => setVigenereKey(e.target.value.toUpperCase().replace(/[^A-Z]/g, ''))}
          placeholder="e.g. LEMON"
        />
      </div>
      <span className="text-[10px] text-slate-500">
        Keyword is case-insensitive. Only alphabetic characters are preserved as key steps.
      </span>
    </div>
  );
}
