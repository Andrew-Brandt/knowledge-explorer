const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
  darkMode: 'class',
  content: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', ...defaultTheme.fontFamily.sans],
        classy: ['Playfair Display', 'serif'],
      },
      colors: {
        light: {
          bg: '#f9f9fb',
          text: '#1e1e1e',
          primary: '#364f6b',
          accent: '#3c6382',
        },
        dark: {
          bg: '#1a1c1f',
          text: '#f0f0f0',
          primary: '#4a90e2',
          accent: '#357ABD',
        },
      },
    },
  },
  plugins: [],
};
