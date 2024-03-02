/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.{html,js}'
  ],
  darkMode: 'media',
  theme: {
    extend: {
      colors: {
        'light': {
          DEFAULT: '#ffffff',
          50: '#ffffff',
          100: '#fafafa',
          200: '#e6e6e6',
          300: '#c7c7c7',
          400: '#a3a3a3',
          500: '#878787',
          600: '#707070',
          700: '#5c5c5c',
          800: '#4f4f4f',
          900: '#474747',
          950: '#333333',
        },
        'dark': {
          50: '#f7f7f7',
          100: '#ebebeb',
          200: '#d4d4d4',
          300: '#b3b3b3',
          400: '#8a8a8a',
          500: '#707070',
          600: '#595959',
          700: '#404040',
          800: '#262626',
          900: '#171717',
          950: '#000000',
          DEFAULT: '#000000',
        },
      }
    },
  },
  plugins: [],
}

