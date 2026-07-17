import { useEffect } from 'react';

interface ToastProps {
  message: string | null;
  type: 'error' | 'success' | 'info';
  onClose: () => void;
}

const typeStyles: Record<ToastProps['type'], string> = {
  error: 'bg-rose-900/90 border-rose-700/50 text-rose-100',
  success: 'bg-emerald-900/90 border-emerald-700/50 text-emerald-100',
  info: 'bg-indigo-900/90 border-indigo-700/50 text-indigo-100',
};

const typeIcons: Record<ToastProps['type'], string> = {
  error: '✕',
  success: '✓',
  info: 'ℹ',
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
        className={`flex items-center gap-3 px-5 py-3 rounded-xl border shadow-2xl backdrop-blur-md min-w-[280px] max-w-md ${typeStyles[type]}`}
      >
        <span className="text-lg font-bold leading-none">{typeIcons[type]}</span>
        <p className="text-sm font-medium flex-1">{message}</p>
        <button
          onClick={onClose}
          className="ml-1 text-current/60 hover:text-current transition-colors text-lg leading-none"
        >
          &times;
        </button>
      </div>
    </div>
  );
}
