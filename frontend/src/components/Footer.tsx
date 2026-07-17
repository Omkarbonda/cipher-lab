export default function Footer() {
  return (
    <footer className="border-t border-ink-600 bg-ink-900 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between text-[10px] text-parchment/30 tracking-[0.1em]">
        <span>&copy; 2026 Cipher Bureau</span>
        <div className="flex items-center gap-3">
          <span className="hover:text-brass/50 transition-colors">FastAPI</span>
          <span className="text-ink-500">|</span>
          <span className="hover:text-brass/50 transition-colors">React 19</span>
          <span className="text-ink-500">|</span>
          <span className="hover:text-brass/50 transition-colors">Tailwind CSS</span>
        </div>
      </div>
    </footer>
  );
}
