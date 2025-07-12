import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router' // Vue Router configuration
import './assets/tailwind.css' // Import Tailwind CSS

const app = createApp(App)

// Initialize Pinia store
const pinia = createPinia()
app.use(pinia)

// Use Vue Router
app.use(router)

app.mount('#app')
