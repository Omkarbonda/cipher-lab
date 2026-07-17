export default function Header() {
  return (
    <header className="border-b border-brass/20 bg-ink-700/80 backdrop-blur-md sticky top-0 z-50 px-6 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          {/* Mechanical cog emblem */}
          <div className="relative w-9 h-9 flex items-center justify-center">
            <svg className="w-9 h-9 text-brass" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <circle cx="12" cy="12" r="3" />
              <path d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
            </svg>
          </div>
          <div>
            <h1 className="text-base font-bold tracking-[0.15em] text-parchment uppercase">
              Cipher Bureau
            </h1>
            <p className="text-[10px] text-brass/70 tracking-[0.2em] uppercase">Classical Cryptanalysis Laboratory</p>
          </div>
        </div>

        <div className="flex items-center gap-2 border border-brass/15 bg-brass/5 rounded px-2.5 py-1">
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full rounded-full bg-brass opacity-40 animate-ping" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-brass" />
          </span>
          <span className="text-[9px] font-bold text-brass/80 tracking-[0.15em] uppercase">Engine Live</span>
        </div>
      </div>
    </header>
  );
}
