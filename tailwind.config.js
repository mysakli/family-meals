/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./entries/templates/**/*.html",
    "./entries/static/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#10b981', // emerald-500
          dark: '#059669',    // emerald-600
          light: '#34d399',   // emerald-400
        },
        secondary: {
          DEFAULT: '#64748b', // slate-500
          dark: '#475569',    // slate-600
          light: '#94a3b8',   // slate-400
        },
        background: '#f8fafc', // slate-50
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
