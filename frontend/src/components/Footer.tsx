export default function Footer() {
  return (
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
  );
}
