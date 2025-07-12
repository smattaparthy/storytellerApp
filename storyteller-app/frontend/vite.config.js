/// <reference types="vitest" />
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173 // As specified in project details (default for Vite)
  },
  test: {
    globals: true, // Use Vitest global APIs (describe, test, expect, etc.)
    environment: 'jsdom', // Simulate a browser environment for component testing
    deps: {
      // Ensure Vue related deps are processed by Vite for tests
      // This might be needed for some CJS dependencies to work correctly in Vitest
      inline: ['vue', '@vue/test-utils', 'vue-router', 'pinia'],
    },
    // Optional: Setup files for tests (e.g., global mocks, Vue testing library config)
    // setupFiles: './src/tests/setup.js',
    coverage: {
      provider: 'v8', // or 'istanbul'
      reporter: ['text', 'json', 'html'],
      reportsDirectory: './coverage'
    }
  }
})
