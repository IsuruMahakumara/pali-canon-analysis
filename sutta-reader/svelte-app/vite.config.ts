import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],
  server: {
    port: 7000,
    proxy: {
      '/api': 'http://localhost:8000',
      '/graphql': 'http://localhost:8000'
    }
  },
  build: {
    outDir: '../static-svelte',
    emptyOutDir: true
  }
});
