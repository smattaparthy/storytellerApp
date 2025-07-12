<template>
  <div class="story-picker p-6 bg-white shadow-xl rounded-lg max-w-lg mx-auto">
    <h2 class="text-2xl font-bold text-primary-purple mb-6 text-center">Create Your Story!</h2>

    <form @submit.prevent="handleGenerateStory" class="space-y-6">
      <div>
        <label for="mainCharacter" class="block text-sm font-medium text-gray-700 mb-1">Choose a Main Character:</label>
        <select
          id="mainCharacter"
          v-model="selectedMainCharacterId"
          class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-primary-purple focus:border-primary-purple sm:text-sm"
          required
        >
          <option disabled value="">Please select one</option>
          <option v-for="char in availableCharacters" :key="char.id" :value="char.id">
            {{ char.emoji }} {{ char.name }}
          </option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Choose Supporting Friends (up to 2):</label>
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-2">
          <div v-for="char in availableCharacters" :key="`support-${char.id}`"
               class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-purple-50 transition-colors"
               :class="{'bg-purple-100 border-primary-purple ring-2 ring-primary-purple': selectedSupportingCharacterIds.includes(char.id)}"
               @click="toggleSupportCharacter(char.id)">
            <input
              type="checkbox"
              :id="`support-char-${char.id}`"
              :value="char.id"
              v-model="selectedSupportingCharacterIds"
              class="h-4 w-4 text-primary-purple border-gray-300 rounded focus:ring-primary-purple hidden"
              :disabled="selectedSupportingCharacterIds.length >= 2 && !selectedSupportingCharacterIds.includes(char.id)"
            />
            <label :for="`support-char-${char.id}`" class="ml-2 text-sm text-gray-700 cursor-pointer">
              {{ char.emoji }} {{ char.name }}
            </label>
          </div>
        </div>
        <p v.if="selectedSupportingCharacterIds.length >= 2" class="text-xs text-gray-500 mt-1">Maximum 2 supporting friends selected.</p>
      </div>

      <div>
        <label for="storyTheme" class="block text-sm font-medium text-gray-700 mb-1">Story Theme:</label>
        <input
          type="text"
          id="storyTheme"
          v-model="storyTheme"
          placeholder="e.g., A Brave Adventure, A Funny Mix-up"
          class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-primary-purple focus:border-primary-purple sm:text-sm"
          required
        />
      </div>

      <button
        type="submit"
        :disabled="storyStore.isLoading || !selectedMainCharacterId"
        class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-lg text-md font-medium text-white bg-gradient-to-r from-primary-pink to-primary-purple hover:from-primary-pink hover:to-pink-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-purple disabled:opacity-50 disabled:cursor-not-allowed transition-all ease-in-out duration-150"
      >
        <span v-if="storyStore.isLoading">Generating... ✨</span>
        <span v-else>Make My Story!</span>
      </button>
    </form>

    <div v-if="storyStore.error" class="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-md">
      <p><strong>Oops! Something went wrong:</strong></p>
      <p>{{ storyStore.error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useStoryStore } from '../stores/storyStore';
import { useRouter } from 'vue-router';

const storyStore = useStoryStore();
const router = useRouter();

const selectedMainCharacterId = ref('');
const selectedSupportingCharacterIds = ref([]);
const storyTheme = ref('A Fun Adventure'); // Default theme

// Fetch characters when component is mounted
onMounted(() => {
  if (storyStore.characters.length === 0) {
    storyStore.fetchCharacters();
  }
});

// Computed property to get characters from the store
const availableCharacters = computed(() => storyStore.characters);

const toggleSupportCharacter = (charId) => {
  if (selectedMainCharacterId.value === charId) return; // Cannot select main character as support

  const index = selectedSupportingCharacterIds.value.indexOf(charId);
  if (index > -1) {
    selectedSupportingCharacterIds.value.splice(index, 1);
  } else {
    if (selectedSupportingCharacterIds.value.length < 2) {
      selectedSupportingCharacterIds.value.push(charId);
    }
  }
};

const handleGenerateStory = async () => {
  if (!selectedMainCharacterId.value || !storyTheme.value) {
    alert('Please select a main character and enter a story theme.');
    return;
  }

  const generationParams = {
    main_character_id: selectedMainCharacterId.value,
    // Filter out main character from supporting, just in case (though UI prevents it)
    supporting_character_ids: selectedSupportingCharacterIds.value.filter(id => id !== selectedMainCharacterId.value),
    story_theme: storyTheme.value,
  };

  try {
    const newStory = await storyStore.generateStory(generationParams);
    if (newStory && newStory.id) {
      // Navigate to the story reading page
      router.push({ name: 'StoryRead', params: { id: newStory.id } });
    } else {
      // Error handled by store, message shown in template
    }
  } catch (error) {
    // Error is already set in the store, UI will react.
    // No specific handling needed here unless for additional local effects.
    console.error("Story generation failed in component:", error);
  }
};
</script>

<style scoped>
/* Add any component-specific styles here */
.story-picker {
  /* Example: animation for when it appears */
  animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
