/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        forest: {
          50:  '#f0f7f0',
          100: '#dceddc',
          200: '#bbdcbb',
          300: '#8ec48e',
          400: '#5da85d',
          500: '#3d8b3d',
          600: '#2d6f2d',
          700: '#245824',
          800: '#1e461e',
          900: '#193a19',
          950: '#0c1f0c',
        },
        earth: {
          50:  '#fdf8f0',
          100: '#faefd9',
          200: '#f3d9a8',
          300: '#e9be6c',
          400: '#dea040',
          500: '#c8841f',
          600: '#a66616',
          700: '#864e15',
          800: '#6e4017',
          900: '#5c3516',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-dot': 'pulseDot 1.4s ease-in-out infinite',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseDot: {
          '0%, 80%, 100%': { transform: 'scale(0.6)', opacity: '0.4' },
          '40%': { transform: 'scale(1)', opacity: '1' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
    },
  },
  plugins: [],
}
