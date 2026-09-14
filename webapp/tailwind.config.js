/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cinema: {
          bg: "#0c0f17",
          card: "#161b26",
          cardHover: "#1c2230",
          border: "#252e42",
          text: "#f1f5f9",
          muted: "#94a3b8",
        },
        like: "#10b981",
        dislike: "#f43f5e",
        watch: "#f59e0b",
        tg: "#2481cc",
        kp: "#f26100",
      },
      boxShadow: {
        'card': '0 10px 25px -5px rgba(0, 0, 0, 0.6), 0 8px 10px -6px rgba(0, 0, 0, 0.5)',
        'card-lg': '0 20px 35px -5px rgba(0, 0, 0, 0.8), 0 12px 15px -7px rgba(0, 0, 0, 0.6)',
        'glow-like': '0 0 25px -5px rgba(16, 185, 129, 0.4)',
        'glow-dislike': '0 0 25px -5px rgba(244, 63, 94, 0.4)',
        'glow-watch': '0 0 25px -5px rgba(245, 158, 11, 0.4)',
      },
    },
  },
  plugins: [],
}

