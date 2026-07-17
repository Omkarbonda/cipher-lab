interface ColumnarConfigProps {
  columnarKey: string;
  setColumnarKey: (key: string) => void;
}

export default function ColumnarConfig({ columnarKey, setColumnarKey }: ColumnarConfigProps) {
  return (
    <div className="flex flex-col space-y-3">
      <div className="flex flex-col space-y-1">
        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Columnar Key</label>
        <input
          type="text"
          className="bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-sm text-slate-200 font-mono focus:outline-none focus:border-indigo-500/80 transition-colors"
          value={columnarKey}
          onChange={(e) => setColumnarKey(e.target.value.toUpperCase().replace(/[^A-Z]/g, ''))}
          placeholder="e.g. KEY"
        />
      </div>
      <span className="text-[10px] text-slate-500">
        Text is written row-wise and read column-wise in the order determined by the sorted keyword columns.
      </span>
    </div>
  );
}
