export default function Header() {
  return (
    <header className="border-b border-slate-800/80 bg-slate-900/40 backdrop-blur-md sticky top-0 z-50 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-violet-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-indigo-200 via-slate-100 to-violet-200 bg-clip-text text-transparent">
              Cipher Lab & Secure Vault
            </h1>
            <p className="text-xs text-slate-400">Interactive Cryptography & Cryptanalysis Laboratory</p>
          </div>
        </div>

        <div className="flex items-center space-x-2 bg-emerald-500/10 border border-emerald-500/20 rounded-full px-3 py-1">
          <span className="relative flex h-1.5 w-1.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-emerald-500"></span>
          </span>
          <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">
            Connected to Engine
          </span>
        </div>
      </div>
    </header>
  );
}
