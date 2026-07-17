interface RailFenceConfigProps {
  rails: number;
  setRails: (rails: number) => void;
}

export default function RailFenceConfig({ rails, setRails }: RailFenceConfigProps) {
  return (
    <div className="flex flex-col space-y-3">
      <div className="flex items-center justify-between text-sm">
        <span className="text-slate-400">Number of Rails (R)</span>
        <span className="font-mono text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/25">{rails}</span>
      </div>
      <input
        type="range"
        min="2"
        max="10"
        value={rails}
        onChange={(e) => setRails(parseInt(e.target.value))}
        className="w-full h-2 bg-slate-900 border border-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500"
      />
      <div className="flex justify-between text-[10px] font-mono text-slate-600">
        <span>2 rails</span>
        <span>6 rails</span>
        <span>10 rails</span>
      </div>
    </div>
  );
}
