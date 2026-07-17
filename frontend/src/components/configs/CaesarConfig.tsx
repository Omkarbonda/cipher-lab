interface CaesarConfigProps {
  caesarShift: number;
  setCaesarShift: (shift: number) => void;
}

export default function CaesarConfig({ caesarShift, setCaesarShift }: CaesarConfigProps) {
  return (
    <div className="flex flex-col space-y-3">
      <div className="flex items-center justify-between text-sm">
        <span className="text-slate-400">Shift Key value (K)</span>
        <span className="font-mono text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/25">{caesarShift}</span>
      </div>
      <input
        type="range"
        min="0"
        max="25"
        value={caesarShift}
        onChange={(e) => setCaesarShift(parseInt(e.target.value))}
        className="w-full h-2 bg-slate-900 border border-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500"
      />
      <div className="flex justify-between text-[10px] font-mono text-slate-600">
        <span>0 (No shift)</span>
        <span>13 (ROT13)</span>
        <span>25</span>
      </div>
    </div>
  );
}
