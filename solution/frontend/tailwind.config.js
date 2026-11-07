/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        europress: {
          blue: '#004B87',
          dark: '#0A2540',
          accent: '#00A3E0',
          warning: '#F59E0B',
          danger: '#EF4444',
          success: '#10B981',
          bg: '#F8FAFC',
          card: '#FFFFFF'
        }
      }
    },
  },
  plugins: [],
}
