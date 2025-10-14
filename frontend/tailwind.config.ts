import type { Config } from "tailwindcss";

export default {
  darkMode: "class",
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0b0f14",
        card: "#10151b",
        ink: "#dbe4ee",
        mute: "#7a8aa0",
        brand: "#53d6a4"
      },
      borderRadius: { xl2: "1.25rem" }
    }
  },
  plugins: []
} satisfies Config;
