/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./eldercare_finance_platform/templates/**/*.html",
    "./eldercare_finance_platform/static/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#4B6BFB',
          DEFAULT: '#3B5BDB',
          dark: '#2B4BD8',
        },
        secondary: {
          light: '#38B2AC',
          DEFAULT: '#319795',
          dark: '#2C7A7B',
        },
        neutral: {
          lightest: '#F7FAFC',
          light: '#EDF2F7',
          DEFAULT: '#E2E8F0',
          dark: '#CBD5E0',
          darkest: '#A0AEC0',
        },
      },
    },
  },
  plugins: [],
}
