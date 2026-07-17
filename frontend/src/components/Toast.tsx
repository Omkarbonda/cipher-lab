import { useEffect } from 'react';

interface ToastProps {
  message: string | null;
  type: 'error' | 'success' | 'info';
  onClose: () => void;
}

const typeStyles: Record<ToastProps['type'], string> = {
  error: 'bg-ink-600 border-red-800/50 text-red-300',
  success: 'bg-ink-600 border-emerald-800/50 text-emerald-300',
  info: 'bg-ink-600 border-brass/30 text-brass/90',
};

export default function Toast({ message, type, onClose }: ToastProps) {
  useEffect(() => {
    if (!message) return;
    const timer = setTimeout(onClose, 4000);
    return () => clearTimeout(timer);
  }, [message, onClose]);

  if (!message) return null;

  return (
    <div className="fixed bottom-6 right-6 z-[100] animate-slide-in">
      <div
        className={`flex items-center gap-3 px-4 py-2.5 border shadow-2xl min-w-[260px] max-w-md font-mono text-sm ${typeStyles[type]}`}
      >
        <span className="font-mono text-lg leading-none opacity-70">
          {type === 'error' ? '!' : type === 'success' ? 'OK' : 'i'}
        </span>
        <p className="flex-1 text-[12px] tracking-[0.02em]">{message}</p>
        <button
          onClick={onClose}
          className="opacity-40 hover:opacity-80 transition-opacity text-sm"
        >
          x
        </button>
      </div>
    </div>
  );
}
