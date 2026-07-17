import React, { useEffect, useState } from 'react';

interface HealthResponse {
  status: string;
}

function App() {
  const [connectionStatus, setConnectionStatus] = useState<'loading' | 'connected' | 'failed'>('loading');
  const [apiData, setApiData] = useState<HealthResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState<string>('');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch('/api/health');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setApiData(data);
        if (data.status === 'ok') {
          setConnectionStatus('connected');
        } else {
          setConnectionStatus('failed');
          setErrorMsg('API returned status: ' + JSON.stringify(data));
        }
      } catch (err: any) {
        setConnectionStatus('failed');
        setErrorMsg(err.message || 'Failed to connect to API');
      }
    };

    checkHealth();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between font-sans selection:bg-indigo-500 selection:text-white">
      {/* Top Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50 px-6 py-4">
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
              <p className="text-xs text-slate-400">Cryptography & Cryptanalysis Playground</p>
            </div>
          </div>

          {/* Connection Indicator */}
          <div className="flex items-center space-x-3 bg-slate-900 border border-slate-800 rounded-full px-4 py-1.5">
            <span className="relative flex h-2 w-2">
              {connectionStatus === 'connected' && (
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              )}
              {connectionStatus === 'loading' && (
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
              )}
              {connectionStatus === 'failed' && (
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
              )}
              <span className={`relative inline-flex rounded-full h-2 w-2 ${
                connectionStatus === 'connected' ? 'bg-emerald-500' :
                connectionStatus === 'loading' ? 'bg-amber-500' : 'bg-rose-500'
              }`}></span>
            </span>
            <span className="text-xs font-medium tracking-wide">
              {connectionStatus === 'connected' && 'API: CONNECTED'}
              {connectionStatus === 'loading' && 'API: CONNECTING...'}
              {connectionStatus === 'failed' && 'API: DISCONNECTED'}
            </span>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-grow max-w-7xl mx-auto px-6 py-12 flex flex-col justify-center items-center">
        <div className="w-full max-w-3xl text-center mb-12">
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase tracking-widest">
            Phase 1 Complete ✓
          </span>
          <h2 className="text-4xl md:text-5xl font-extrabold tracking-tight mt-4 mb-6 text-slate-100">
            Backend Engine Ready
          </h2>
          <p className="text-slate-400 text-lg max-w-xl mx-auto leading-relaxed">
            4 classical ciphers implemented and tested (46/46 ✅). FastAPI backend and React frontend are connected. Phase 2 — cryptanalysis — coming next.
          </p>
        </div>

        {/* Integration Status Box */}
        <div className="w-full max-w-lg bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-2xl backdrop-blur-sm mb-12">
          <div className="flex items-center justify-between mb-4 border-b border-slate-800/80 pb-4">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Health Status</span>
            <span className="text-xs text-slate-500 font-mono">GET /api/health</span>
          </div>

          {connectionStatus === 'loading' && (
            <div className="py-6 flex flex-col items-center justify-center space-y-3">
              <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
              <p className="text-slate-400 text-sm font-medium animate-pulse">Contacting API...</p>
            </div>
          )}

          {connectionStatus === 'connected' && (
            <div className="space-y-4">
              <div className="flex items-center space-x-3 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-xl p-4">
                <svg className="w-6 h-6 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div className="text-left">
                  <div className="font-semibold text-sm">Integration Verified</div>
                  <div className="text-xs opacity-90">Frontend is proxying API calls correctly.</div>
                </div>
              </div>
              <div className="bg-slate-950 rounded-lg p-4 font-mono text-xs text-left border border-slate-800">
                <div className="text-slate-500">// Response Payload</div>
                <pre className="text-indigo-300 mt-1">{JSON.stringify(apiData, null, 2)}</pre>
              </div>
            </div>
          )}

          {connectionStatus === 'failed' && (
            <div className="space-y-4">
              <div className="flex items-center space-x-3 bg-rose-500/10 text-rose-400 border border-rose-500/20 rounded-xl p-4">
                <svg className="w-6 h-6 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div className="text-left">
                  <div className="font-semibold text-sm">Connection Failed</div>
                  <div className="text-xs opacity-90">Make sure the backend FastAPI server is running on port 8000.</div>
                </div>
              </div>
              <div className="bg-slate-950 rounded-lg p-4 font-mono text-xs text-left border border-slate-800 text-rose-300">
                <div className="text-slate-500">// Error Message</div>
                <div className="mt-1">{errorMsg}</div>
              </div>
            </div>
          )}
        </div>

        {/* Sneak peek of upcoming modules */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-3xl">
          {/* Card 1 */}
          <div className="bg-slate-900/30 border border-slate-800/80 rounded-2xl p-6 relative overflow-hidden group text-left">
            <div className="absolute top-4 right-4 bg-slate-800/50 border border-slate-700/50 rounded-full px-2.5 py-0.5 text-[10px] font-bold text-indigo-400 uppercase">
              Phase 1-4
            </div>
            <div className="w-10 h-10 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center mb-4 text-indigo-400">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 className="font-bold text-lg mb-2 text-slate-200">Cipher Lab</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Interactive simulators for classical ciphers (Caesar, Vigenère, Enigma) with live visualizers (rotors, frequency charts) and cracking tools.
            </p>
            <div className="mt-4 pt-4 border-t border-slate-800/50 flex items-center text-xs text-emerald-500 font-medium">
              <svg className="w-3.5 h-3.5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Phase 1 Done — Caesar, Vigenère, Substitution, Playfair
            </div>
          </div>

          {/* Card 2 */}
          <div className="bg-slate-900/30 border border-slate-800/80 rounded-2xl p-6 relative overflow-hidden group text-left">
            <div className="absolute top-4 right-4 bg-slate-800/50 border border-slate-700/50 rounded-full px-2.5 py-0.5 text-[10px] font-bold text-violet-400 uppercase">
              Phase 5
            </div>
            <div className="w-10 h-10 rounded-lg bg-violet-500/10 border border-violet-500/20 flex items-center justify-center mb-4 text-violet-400">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="font-bold text-lg mb-2 text-slate-200">Secure Vault</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Production-grade modern cryptographic vault utilizing AES-256-GCM, secure key derivations, and passphrase strength estimation.
            </p>
            <div className="mt-4 pt-4 border-t border-slate-800/50 flex items-center text-xs text-slate-500 font-medium">
              <svg className="w-3.5 h-3.5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              Module Locked (Pending Phase 5)
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 px-6 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <p>© 2026 Cipher Lab & Secure Vault. Portfolio Project Scaffolding.</p>
          <div className="flex space-x-4">
            <span className="hover:text-slate-400 transition-colors">FastAPI 1.0</span>
            <span>•</span>
            <span className="hover:text-slate-400 transition-colors">React 19 + TypeScript</span>
            <span>•</span>
            <span className="hover:text-slate-400 transition-colors">Tailwind CSS v3</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
