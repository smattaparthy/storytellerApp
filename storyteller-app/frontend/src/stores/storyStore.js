import { defineStore } from 'pinia'
import axios from 'axios' // Assuming axios is used for API calls

// Define the base URL for the API. Consider moving this to a config file or .env.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const useStoryStore = defineStore('story', {
  state: () => ({
    stories: [],
    currentStory: null,
    isLoading: false,
    error: null,
    characters: [], // To store available characters
    favoriteStories: [],
  }),

  getters: {
    // Example getter: get story by ID
    getStoryById: (state) => (id) => {
      return state.stories.find(story => story.id === parseInt(id)) ||
             state.favoriteStories.find(story => story.id === parseInt(id));
    },
    // All stories including favorites, without duplicates
    allUniqueStories: (state) => {
      const all = [...state.stories, ...state.favoriteStories];
      const unique = [];
      const ids = new Set();
      for (const story of all) {
        if (!ids.has(story.id)) {
          ids.add(story.id);
          unique.push(story);
        }
      }
      return unique;
    }
  },

  actions: {
    // Fetch all available characters
    async fetchCharacters() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await axios.get(`${API_BASE_URL}/characters`);
        this.characters = response.data; // Assuming API returns an array of characters
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Failed to fetch characters';
        console.error("Error fetching characters:", err);
      } finally {
        this.isLoading = false;
      }
    },

    // Generate a new story
    async generateStory(generationParams) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await axios.post(`${API_BASE_URL}/stories/generate`, generationParams);
        const newStory = response.data;
        this.stories.unshift(newStory); // Add to the beginning of the list
        this.currentStory = newStory;
        return newStory; // Return the newly created story
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Failed to generate story';
        console.error("Error generating story:", err);
        throw err; // Re-throw to allow components to handle it
      } finally {
        this.isLoading = false;
      }
    },

    // Fetch all stories
    async fetchStories() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await axios.get(`${API_BASE_URL}/stories`);
        this.stories = response.data;
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Failed to fetch stories';
        console.error("Error fetching stories:", err);
      } finally {
        this.isLoading = false;
      }
    },

    // Fetch favorite stories
    async fetchFavoriteStories() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await axios.get(`${API_BASE_URL}/stories/favorites`);
        this.favoriteStories = response.data;
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Failed to fetch favorite stories';
        console.error("Error fetching favorite stories:", err);
      } finally {
        this.isLoading = false;
      }
    },

    // Fetch formatted pages for a specific story
    async fetchStoryPages(storyId) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await axios.get(`${API_BASE_URL}/stories/${storyId}/pages`);
        // Assuming the response is the pages data. We might want to store this
        // in currentStory.formatted_pages or similar.
        // For now, just returning it.
        if (this.currentStory && this.currentStory.id === parseInt(storyId)) {
            this.currentStory.formatted_pages = response.data;
        } else {
            // If the story is not currentStory, find and update or handle as needed
            const story = this.stories.find(s => s.id === parseInt(storyId)) || this.favoriteStories.find(s => s.id === parseInt(storyId));
            if (story) {
                story.formatted_pages = response.data;
            }
        }
        return response.data;
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || `Failed to fetch pages for story ${storyId}`;
        console.error(`Error fetching pages for story ${storyId}:`, err);
        throw err;
      } finally {
        this.isLoading = false;
      }
    },

    // Action to set a story as current (e.g., when navigating to read it)
    setCurrentStoryById(storyId) {
        this.currentStory = this.getStoryById(storyId) || null;
        if (!this.currentStory) {
            console.warn(`Story with ID ${storyId} not found in store to set as current.`);
        }
    }

    // TODO: Add actions for:
    // - Toggling favorite status (PATCH /stories/{story_id}/favorite)
    // - Deleting a story (DELETE /stories/{story_id})
    // - Loading a single story's full details if needed
  },
})
