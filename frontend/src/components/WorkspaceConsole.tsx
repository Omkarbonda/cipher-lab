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
    <div className="border border-ink-500 bg-ink-700/60">
      {/* Panel header — teletype label strip */}
      <div className="flex items-center justify-between px-4 py-2 bg-ink-600/80 border-b border-ink-500">
        <span className="text-[10px] text-parchment/40 tracking-[0.2em] uppercase">Workspace Console</span>
        <span className="text-[9px] text-brass/50 tracking-[0.15em] uppercase">IN&#47;OUT</span>
      </div>

      <div className="p-4 flex flex-col space-y-4">
        {/* Input area */}
        <div className="flex flex-col space-y-1.5">
          <label className="text-[10px] text-parchment/40 tracking-[0.2em] uppercase">Plaintext / Ciphertext</label>
          <textarea
            className="w-full h-28 bg-ink-900 border border-ink-500 px-4 py-3 text-sm text-parchment/90 placeholder:text-ink-400 focus:outline-none focus:border-brass/40 transition-colors resize-none"
            placeholder="Type message here..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
        </div>

        {/* Action buttons — mechanical switches */}
        <div className="flex items-center gap-3">
          <button
            onClick={handleEncrypt}
            className="flex-1 py-2.5 px-4 border border-brass/40 bg-brass/8 text-brass text-sm font-semibold tracking-[0.1em] uppercase hover:bg-brass/15 active:bg-brass/20 transition-all"
          >
            Encrypt
          </button>
          <button
            onClick={handleDecrypt}
            className="flex-1 py-2.5 px-4 border border-parchment/15 bg-transparent text-parchment/70 text-sm font-semibold tracking-[0.1em] uppercase hover:border-parchment/30 hover:text-parchment/90 transition-all"
          >
            Decrypt
          </button>
          <button
            onClick={handleCrack}
            disabled={isCracking || activeTab === 'substitution' || activeTab === 'playfair'}
            className="flex-1 py-2.5 px-4 border border-amber/30 bg-amber/8 text-amber text-sm font-semibold tracking-[0.1em] uppercase hover:bg-amber/15 transition-all disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {isCracking ? (
              <div className="w-4 h-4 border-2 border-amber/60 border-t-transparent rounded-full animate-spin" />
            ) : (
              'Auto-Crack'
            )}
          </button>
        </div>

        {/* Output area — teletype printout */}
        <div className="flex flex-col space-y-1.5">
          <div className="flex items-center justify-between">
            <label className="text-[10px] text-parchment/40 tracking-[0.2em] uppercase">Output</label>
            {outputText && (
              <button
                onClick={() => { navigator.clipboard.writeText(outputText); }}
                className="text-[9px] text-brass/50 hover:text-brass/80 tracking-[0.15em] uppercase transition-colors"
              >
                Copy
              </button>
            )}
          </div>
          <div className="min-h-24 bg-ink-900 border border-ink-500 px-4 py-3 text-sm text-brass/80 break-all whitespace-pre-wrap select-all relative">
            {outputText ? (
              <span className="animate-fade-in">{outputText}</span>
            ) : (
              <span className="text-ink-400 italic">Awaiting input...</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
