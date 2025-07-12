import { createRouter, createWebHistory } from 'vue-router'

// Import view components (placeholders for now)
// These will be created in the views/ directory
// Example: import HomeView from '../views/HomeView.vue'
// Example: import CreateStoryView from '../views/CreateStoryView.vue'
// Example: import StoryHistoryView from '../views/StoryHistoryView.vue'
// Example: import StoryReadView from '../views/StoryReadView.vue'

// Placeholder components (inline for now, will move to files)
const HomeView = { template: '<div class="text-center p-8"><h1 class="text-4xl font-bold text-primary-purple mb-4">Welcome to Storyteller Fun!</h1><p class="text-lg text-gray-700">Create magical stories for your little ones.</p> <router-link to=\'/create\' class=\'mt-6 inline-block bg-primary-pink text-white font-semibold py-3 px-6 rounded-lg shadow-md hover:bg-opacity-80 transition-all\'>Start Creating!</router-link></div>' }
const CreateStoryView = { template: '<div class="p-8"><h1 class="text-3xl font-bold text-primary-purple mb-6">Create a New Story</h1><!-- Story creation form will go here --> <p class="text-gray-600">Character selection and story theme inputs will be here.</p></div>' }
const StoryHistoryView = { template: '<div class="p-8"><h1 class="text-3xl font-bold text-primary-purple mb-6">My Story Library</h1><!-- List of saved stories will go here --><p class="text-gray-600">A gallery of generated stories will appear here.</p></div>' }
const StoryReadView = { template: '<div class="p-8"><h1 class="text-3xl font-bold text-primary-purple mb-6">Reading Story...</h1><!-- Story book viewer will go here --><p class="text-gray-600">The interactive story book will be displayed here.</p></div>' }
const NotFoundView = { template: '<div class="text-center p-8"><h1 class="text-4xl font-bold text-red-500 mb-4">404 - Page Not Found</h1><p class="text-lg text-gray-700">Oops! The page you are looking for does not exist.</p><router-link to=\'/\' class=\'mt-6 inline-block text-primary-purple hover:underline\'>Go Home</router-link></div>'}


const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView, // To be replaced with actual HomeView component
  },
  {
    path: '/create',
    name: 'CreateStory',
    component: CreateStoryView, // To be replaced
  },
  {
    path: '/history',
    name: 'StoryHistory',
    component: StoryHistoryView, // To be replaced
  },
  {
    path: '/story/:id', // Route for reading a specific story
    name: 'StoryRead',
    component: StoryReadView, // To be replaced
    props: true, // Pass route params as props to the component
  },
  // Add more routes as needed (e.g., favorites, settings)
  {
    path: '/:pathMatch(.*)*', // Catch-all route for 404 Not Found
    name: 'NotFound',
    component: NotFoundView,
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // Use history mode
  routes,
  scrollBehavior(to, from, savedPosition) {
    // Always scroll to top when navigating to a new route
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

export default router
