<template>
  <div id="app-container" class="min-h-screen bg-gradient-to-br from-purple-200 via-pink-100 to-blue-200 text-gray-800">
    <!-- Header/Navbar placeholder -->
    <header class="bg-primary-purple shadow-lg p-4">
      <nav class="container mx-auto flex justify-between items-center">
        <router-link to="/" class="text-2xl font-bold text-white hover:text-accent-yellow transition-colors">
          Storyteller Fun! 📖✨
        </router-link>
        <div>
          <router-link to="/" class="text-white hover:text-accent-yellow px-3 py-2 rounded-md text-sm font-medium">Home</router-link>
          <router-link to="/create" class="text-white hover:text-accent-yellow px-3 py-2 rounded-md text-sm font-medium">Create Story</router-link>
          <router-link to="/history" class="text-white hover:text-accent-yellow px-3 py-2 rounded-md text-sm font-medium">My Stories</router-link>
          <!-- Add more navigation links as needed -->
        </div>
      </nav>
    </header>

    <!-- Main content area where router views will be rendered -->
    <main class="container mx-auto p-4 sm:p-6 lg:p-8">
      <router-view v-slot="{ Component }">
        <transition name="fade-slide" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer placeholder -->
    <footer class="text-center p-4 mt-8 text-sm text-purple-700">
      <p>&copy; {{ new Date().getFullYear() }} Storyteller App. For entertainment purposes only.</p>
    </footer>
  </div>
</template>

<script setup>
// No specific script setup needed for this basic App.vue yet.
// Composition API is enabled by default in Vue 3 script setup.
</script>

<style>
/* Global styles for transitions (can also be in a separate CSS file) */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(10px); /* Slide slightly from bottom */
}

/* Ensuring body takes full height for gradient to show if content is short */
html, body, #app, #app-container {
  min-height: 100vh;
}
#app-container {
  display: flex;
  flex-direction: column;
}
main {
  flex-grow: 1;
}
</style>
