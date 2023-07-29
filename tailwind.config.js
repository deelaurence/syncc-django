/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/main.html",
    "./templates/navbar.html",
    "./base/templates/base/*.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  darkMode: "class",
  theme: {
    screen: {
      sm: "480px",
      bmd: "600px",
      md: "768px",
      lg: "900px",
      xl: "1440px",
    },
    extend: {
      colors: {
        white: "#fafafa",
        dark: "#22303c",
        darker: "#192734",
        darkest: "#15202b",
        darkestTrans: "rgba(21,32,43,0.9)",
        light: "#8899ac",
        opaque: "#B8B8B8",
      },
    },
  },
  plugins: [],
};
