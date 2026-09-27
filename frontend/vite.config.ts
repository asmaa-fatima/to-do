import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Dev: proxy /api to the backend so the browser sees one origin.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: { "/api": process.env.VITE_API_TARGET ?? "http://localhost:8000" },
  },
});
