const colors = require('tailwindcss/colors')

module.exports = {
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        sans: 'Work Sans',
      },
      colors: {
        blue: colors.sky,
        gray: colors.warmGray,
        indigo: colors.indigo,
        yellow: colors.yellow,
        green: colors.green
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
