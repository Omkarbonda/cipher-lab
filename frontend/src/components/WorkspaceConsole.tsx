import type { CipherType } from '../types/cipher';

interface WorkspaceConsoleProps {
  inputText: string;
  setInputText: (text: string) => void;
  outputText: string;
  handleEncrypt: () => void;
  handleDecrypt: () => void;
  handleCrack: () => void;
  isCracking: boolean;
  activeTab: CipherType;
}

export default function WorkspaceConsole({
  inputText,
  setInputText,
  outputText,
  handleEncrypt,
  handleDecrypt,
  handleCrack,
  isCracking,
  activeTab,
}: WorkspaceConsoleProps) {
  return (
    <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-sm flex flex-col space-y-4">
      <h2 className="text-lg font-bold text-slate-200 flex items-center">
        <svg className="w-5 h-5 mr-2 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
        </svg>
        Workspace Console
      </h2>

      {/* Input area */}
      <div className="flex flex-col space-y-1.5">
        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Input Plaintext / Ciphertext</label>
        <textarea
          className="w-full h-32 bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-indigo-500/80 transition-colors font-mono resize-none"
          placeholder="Type your message here..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
      </div>

      {/* Core Action buttons */}
      <div className="flex items-center gap-3 pt-2">
        <button
          onClick={handleEncrypt}
          className="flex-1 py-3 px-4 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 text-white font-semibold text-sm transition-all shadow-lg shadow-indigo-600/10 active:scale-[0.98]"
        >
          🔐 Encrypt Message
        </button>
        <button
          onClick={handleDecrypt}
          className="flex-1 py-3 px-4 rounded-xl bg-slate-800 border border-slate-700 hover:bg-slate-700/85 text-slate-200 font-semibold text-sm transition-all active:scale-[0.98]"
        >
          🔓 Decrypt Message
        </button>
        <button
          onClick={handleCrack}
          disabled={isCracking || activeTab === 'substitution' || activeTab === 'playfair'}
          className="px-5 py-3 rounded-xl bg-violet-600/20 hover:bg-violet-600/30 border border-violet-500/30 hover:border-violet-500/50 text-violet-300 font-semibold text-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-w-[120px]"
        >
          {isCracking ? (
            <div className="w-5 h-5 border-2 border-violet-400 border-t-transparent rounded-full animate-spin"></div>
          ) : (
            '⚡ Auto-Crack'
          )}
        </button>
      </div>

      {/* Output area */}
      <div className="flex flex-col space-y-1.5 pt-2">
        <div className="flex items-center justify-between">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Output Result</label>
          {outputText && (
            <button
              onClick={() => { navigator.clipboard.writeText(outputText); }}
              className="text-[10px] text-indigo-400 hover:text-indigo-300 font-semibold uppercase"
            >
              Copy to Clipboard
            </button>
          )}
        </div>
        <div className={`w-full min-h-24 bg-slate-950 border border-slate-800/80 rounded-xl px-4 py-3 text-sm text-indigo-300 font-mono break-all whitespace-pre-wrap select-all relative ${outputText ? 'animate-fade-in' : ''}`}>
          {outputText || <span className="text-slate-600">The result will appear here...</span>}
        </div>
      </div>
    </div>
  );
}
