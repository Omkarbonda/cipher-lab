interface AffineConfigProps {
  affineA: number;
  setAffineA: (a: number) => void;
  affineB: number;
  setAffineB: (b: number) => void;
}

function gcd(a: number, b: number): number {
  a = Math.abs(a);
  b = Math.abs(b);
  while (b) {
    [a, b] = [b, a % b];
  }
  return a;
}

export default function AffineConfig({ affineA, setAffineA, affineB, setAffineB }: AffineConfigProps) {
  const isCoprime = gcd(affineA, 26) === 1;

  return (
    <div className="flex flex-col space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="flex flex-col space-y-1">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Multiplier (a)</label>
          <input
            type="number"
            min={1}
            max={25}
            className={`bg-slate-950 border ${!isCoprime ? 'border-rose-500/60' : 'border-slate-800'} rounded-xl px-4 py-2 text-sm text-slate-200 font-mono focus:outline-none focus:border-indigo-500/80 transition-colors`}
            value={affineA}
            onChange={(e) => setAffineA(parseInt(e.target.value) || 0)}
          />
          <span className="text-[10px] text-slate-500">Must be coprime with 26</span>
        </div>
        <div className="flex flex-col space-y-1">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Shift (b)</label>
          <input
            type="number"
            min={0}
            max={25}
            className="bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-sm text-slate-200 font-mono focus:outline-none focus:border-indigo-500/80 transition-colors"
            value={affineB}
            onChange={(e) => setAffineB(parseInt(e.target.value) || 0)}
          />
          <span className="text-[10px] text-slate-500">Value between 0 and 25</span>
        </div>
      </div>
      {!isCoprime && (
        <span className="text-[10px] text-rose-400 font-medium">
          ⚠️ gcd({affineA}, 26) = {gcd(affineA, 26)} — 'a' must be coprime with 26 for decryption to work.
        </span>
      )}
    </div>
  );
}
