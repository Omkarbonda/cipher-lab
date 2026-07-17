/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'monospace'],
        sans: ['"JetBrains Mono"', 'ui-monospace', 'system-ui', 'sans-serif'],
      },
      colors: {
        ink: {
          DEFAULT: '#0d0c0a',
          50: '#f0ede8',
          100: '#d8d2c8',
          200: '#b0a890',
          300: '#8a7e66',
          400: '#5c5340',
          500: '#3d3628',
          600: '#2a251b',
          700: '#1a1815',
          800: '#12100e',
          900: '#0d0c0a',
        },
        brass: {
          DEFAULT: '#c9a84c',
          50: '#faf6ea',
          100: '#f0e5c0',
          200: '#e0cc82',
          300: '#d4b854',
          400: '#c9a84c',
          500: '#b8923a',
          600: '#9a7830',
          700: '#7a5e26',
          800: '#5c4620',
          900: '#3d2e18',
        },
        amber: {
          DEFAULT: '#d4a853',
          50: '#fdf8ee',
          100: '#f9ecc8',
          200: '#f2d78a',
          300: '#e8be54',
          400: '#d4a853',
          500: '#b88d35',
          600: '#9a7428',
          700: '#7a5a1e',
          800: '#5c4418',
          900: '#3d2e12',
        },
        parchment: {
          DEFAULT: '#e8e0d0',
          50: '#faf7f0',
          100: '#f0ece0',
          200: '#e8e0d0',
          300: '#d0c8b0',
          400: '#b0a890',
          500: '#908870',
          600: '#706850',
          700: '#504840',
          800: '#302830',
          900: '#201820',
        },
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0', transform: 'translateY(6px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'slide-in': {
          '0%': { transform: 'translateX(100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        'pulse-glow': {
          '0%, 100%': { boxShadow: '0 0 4px rgba(201, 168, 76, 0.3)' },
          '50%': { boxShadow: '0 0 12px rgba(201, 168, 76, 0.6)' },
        },
        'scan-line': {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' },
        },
      },
      animation: {
        'fade-in': 'fade-in 0.35s ease-out both',
        'slide-in': 'slide-in 0.3s ease-out',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'scan-line': 'scan-line 4s linear infinite',
      },
    },
  },
  plugins: [],
}
