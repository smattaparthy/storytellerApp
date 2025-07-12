<template>
  <div class="storybook-viewer max-w-3xl mx-auto bg-white shadow-2xl rounded-lg overflow-hidden">
    <div v-if="isLoading" class="p-10 text-center">
      <p class="text-xl text-primary-purple animate-pulse">Loading your amazing story... ✨</p>
    </div>
    <div v-else-if="error" class="p-10 text-center text-red-600">
      <p><strong>Oh no! We couldn't load the story:</strong></p>
      <p>{{ error }}</p>
      <router-link to="/create" class="mt-4 inline-block bg-primary-pink text-white px-4 py-2 rounded hover:bg-opacity-80">Try Creating Again</router-link>
    </div>
    <div v-else-if="!currentStory || !storyPages.length" class="p-10 text-center text-gray-600">
      <p>Story not found or no pages available.</p>
      <router-link to="/history" class="mt-4 inline-block bg-primary-purple text-white px-4 py-2 rounded hover:bg-opacity-80">See My Stories</router-link>
    </div>

    <div v-else class="book-container relative aspect-[2/1]"> <!-- Aspect ratio for two pages side-by-side -->
      <!-- Story Title -->
      <h1 class="absolute top-4 left-1/2 -translate-x-1/2 text-center text-xl sm:text-2xl font-bold text-purple-700 z-20 px-4 py-1 bg-white/80 rounded-md shadow">
        {{ currentStory.title }}
      </h1>

      <!-- Page Display Area -->
      <div class="page-display flex w-full h-full">
        <!-- Left Page -->
        <div class="page left-page w-1/2 p-4 sm:p-6 border-r border-gray-300 flex flex-col justify-between overflow-y-auto" :class="pageTransitionClass">
          <div v-if="currentPageIndex > 0 && storyPages[currentPageIndex - 1]" class="page-content">
            <img v-if="storyPages[currentPageIndex - 1].image_data_base64 && storyPages[currentPageIndex - 1].layout !== 'image_right'"
                 :src="'data:image/png;base64,' + storyPages[currentPageIndex - 1].image_data_base64"
                 alt="Story image"
                 class="mb-3 rounded-lg shadow-md w-full h-auto max-h-48 object-contain"
                 :class="{'float-left mr-3 w-1/2': storyPages[currentPageIndex - 1].layout === 'image_left'}"/>
            <p class="text-sm sm:text-base leading-relaxed whitespace-pre-line"
               :class="{'clear-left': storyPages[currentPageIndex - 1].layout === 'image_left'}">
              {{ storyPages[currentPageIndex - 1].text }}
            </p>
          </div>
           <div v-else class="flex items-center justify-center h-full">
            <span class="text-gray-400 text-center">End of the story...<br>or the beginning!</span>
          </div>
          <span class="block text-left text-xs text-gray-500 mt-auto pt-2">{{ storyPages[currentPageIndex - 1] ? storyPages[currentPageIndex - 1].page_num : '' }}</span>
        </div>

        <!-- Right Page -->
        <div class="page right-page w-1/2 p-4 sm:p-6 flex flex-col justify-between overflow-y-auto" :class="pageTransitionClass">
          <div v-if="storyPages[currentPageIndex]" class="page-content">
            <img v-if="storyPages[currentPageIndex].image_data_base64 && storyPages[currentPageIndex].layout !== 'image_left'"
                 :src="'data:image/png;base64,' + storyPages[currentPageIndex].image_data_base64"
                 alt="Story image"
                 class="mb-3 rounded-lg shadow-md w-full h-auto max-h-48 object-contain"
                 :class="{'float-right ml-3 w-1/2': storyPages[currentPageIndex].layout === 'image_right'}"/>
            <p class="text-sm sm:text-base leading-relaxed whitespace-pre-line"
               :class="{'clear-right': storyPages[currentPageIndex].layout === 'image_right'}">
              {{ storyPages[currentPageIndex].text }}
            </p>
          </div>
          <div v-else class="flex items-center justify-center h-full">
            <span class="text-gray-400">The End!</span>
          </div>
          <span class="block text-right text-xs text-gray-500 mt-auto pt-2">{{ storyPages[currentPageIndex] ? storyPages[currentPageIndex].page_num : '' }}</span>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <button @click="prevPage" :disabled="currentPageIndex <= 0"
              class="nav-button prev-button absolute left-2 sm:left-4 top-1/2 -translate-y-1/2 z-10 bg-white/70 hover:bg-primary-purple/80 text-purple-700 hover:text-white p-2 rounded-full shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed">
        ➔ <!-- Left Arrow (rotated) -->
      </button>
      <button @click="nextPage" :disabled="currentPageIndex >= storyPages.length -1"
              class="nav-button next-button absolute right-2 sm:right-4 top-1/2 -translate-y-1/2 z-10 bg-white/70 hover:bg-primary-purple/80 text-purple-700 hover:text-white p-2 rounded-full shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed">
        ➔
      </button>
    </div>
     <div class="p-4 text-center border-t mt-2" v-if="currentStory">
        <button @click="goBackToHistory" class="text-sm text-primary-purple hover:underline">Back to My Stories</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useStoryStore } from '../stores/storyStore';
import { useRoute, useRouter } from 'vue-router';

const props = defineProps({
  id: { // Story ID from route params
    type: [String, Number],
    required: true
  }
});

const storyStore = useStoryStore();
const route = useRoute();
const router = useRouter();

const currentPageIndex = ref(0); // Index for the right page (e.g., 0 means page 1 is on right)
const storyPages = ref([]);
const pageTransitionClass = ref('');

const isLoading = computed(() => storyStore.isLoading);
const error = computed(() => storyStore.error);
const currentStory = computed(() => storyStore.currentStory);

const loadStoryData = async () => {
  const storyId = parseInt(props.id);
  storyStore.setCurrentStoryById(storyId); // Try to load from existing stories first

  if (!currentStory.value || !currentStory.value.formatted_pages) {
    try {
      // If not found or pages not loaded, fetch them
      const pages = await storyStore.fetchStoryPages(storyId);
      storyPages.value = pages || [];
      // If currentStory wasn't set by setCurrentStoryById (e.g. direct navigation),
      // we might need to fetch the story details too, or rely on fetchStoryPages to populate it.
      // For now, assume fetchStoryPages might also update currentStory or we get title elsewhere.
      // A better approach might be a dedicated `fetchStoryDetails(storyId)` action.
      if (!currentStory.value && storyStore.getStoryById(storyId)) {
         storyStore.setCurrentStoryById(storyId); // Re-set if it was fetched by another action
      }

    } catch (e) {
      console.error("Failed to load story pages in component:", e);
      // Error is handled by store and displayed via computed property
    }
  } else if (currentStory.value && currentStory.value.formatted_pages) {
    storyPages.value = currentStory.value.formatted_pages;
  }

  currentPageIndex.value = 0; // Reset to first page
};

onMounted(loadStoryData);
watch(() => props.id, loadStoryData); // Re-load if story ID changes

const triggerPageTransition = () => {
  pageTransitionClass.value = 'page-turn-active';
  setTimeout(() => {
    pageTransitionClass.value = '';
  }, 300); // Duration of the CSS animation
};

const nextPage = () => {
  if (currentPageIndex.value < storyPages.value.length -1 ) { // current page on right is not the last
    triggerPageTransition();
    currentPageIndex.value += 2; // Show next two pages
    // If only one page left, currentPageIndex might point to an empty right page.
    // The template handles this by showing "The End".
    // Ensure we don't go out of bounds for the right page if it's the very last one.
    if (currentPageIndex.value >= storyPages.value.length) {
        currentPageIndex.value = storyPages.value.length -1; // Last page on right, left might be blank or previous
    }

  }
};

const prevPage = () => {
  if (currentPageIndex.value > 0) {
    triggerPageTransition();
    currentPageIndex.value -= 2;
    if (currentPageIndex.value < 0) currentPageIndex.value = 0;
  }
};

const goBackToHistory = () => {
  router.push({ name: 'StoryHistory' });
};

</script>

<style scoped>
.storybook-viewer {
  /* font-family: 'Comic Sans MS', 'Arial Rounded MT Bold', sans-serif; /* Child-friendly font */
  min-height: 70vh; /* Ensure it takes up some space */
}

.book-container {
  /* Simulates an open book */
  background-color: #fff8f0; /* Creamy paper color */
}

.page {
  box-sizing: border-box;
  /* overflow: hidden; /* Prevent scrollbars within a page, content should fit */
  transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out;
}

.page-turn-active {
  opacity: 0.7;
  transform: scale(0.98); /* Slight shrink effect */
}

.page-content {
  flex-grow: 1;
}

.nav-button.prev-button {
  transform: translateY(-50%) rotate(180deg); /* Point left */
}
.nav-button.next-button {
   /* Point right (default arrow) */
}

/* Responsive text, images */
.page img {
  display: block; /* Ensure images are block for margin auto etc. */
  margin-left: auto;
  margin-right: auto;
}

.page p {
  /* Add more styling for text if needed */
}

/* Hide scrollbar for page content but allow scrolling */
.page {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none;  /* IE and Edge */
}
.page::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

</style>
