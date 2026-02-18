/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'dino': {
                    primary: '#00ff9f',
                    'primary-glow': 'rgba(0, 255, 159, 0.6)',
                    secondary: '#ff006e',
                    'secondary-glow': 'rgba(255, 0, 110, 0.6)',
                    accent: '#ffbe0b',
                    'accent-glow': 'rgba(255, 190, 11, 0.6)',
                    background: '#0a0e27',
                    surface: '#1a1f3a',
                    text: '#e0e0e0',
                    'text-dim': '#8892b0',
                }
            },
            fontFamily: {
                'cyber': ['Orbitron', 'sans-serif'],
                'mono': ['Share Tech Mono', 'monospace'],
            },
            boxShadow: {
                'neon-green': '0 0 20px rgba(0, 255, 159, 0.6)',
                'neon-pink': '0 0 20px rgba(255, 0, 110, 0.6)',
                'neon-yellow': '0 0 20px rgba(255, 190, 11, 0.6)',
            },
            animation: {
                'glitch': 'glitch 1s infinite',
                'scan': 'scan 8s linear infinite',
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            },
            keyframes: {
                glitch: {
                    '0%, 100%': { transform: 'translate(0)' },
                    '20%': { transform: 'translate(-2px, 2px)' },
                    '40%': { transform: 'translate(-2px, -2px)' },
                    '60%': { transform: 'translate(2px, 2px)' },
                    '80%': { transform: 'translate(2px, -2px)' },
                },
                scan: {
                    '0%': { transform: 'translateY(-100%)' },
                    '100%': { transform: 'translateY(100vh)' },
                }
            }
        },
    },
    plugins: [],
}
