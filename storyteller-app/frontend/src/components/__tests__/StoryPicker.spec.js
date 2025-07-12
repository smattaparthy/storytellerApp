import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { useStoryStore } from '../../stores/storyStore'; // Adjust path as needed
import StoryPicker from '../StoryPicker.vue'; // Adjust path as needed
import router from '../../router'; // Import router instance

// Mock Vue Router
vi.mock('vue-router', async () => {
  const actualRouter = await vi.importActual('vue-router');
  return {
    ...actualRouter,
    useRouter: () => ({
      push: vi.fn(), // Mock the push function
    }),
  };
});


describe('StoryPicker.vue', () => {
  let pinia;

  beforeEach(() => {
    // Create a new Pinia instance and make it active for each test
    pinia = createPinia();
    setActivePinia(pinia);

    // Reset mocks if any were used directly on store actions (alternative to store setup below)
    // vi.clearAllMocks(); // if you were mocking store actions directly
  });

  it('renders the component and form elements', () => {
    const wrapper = mount(StoryPicker, {
      global: {
        plugins: [pinia, router], // Provide pinia and router instance
      },
    });

    // Check if the main heading is present
    expect(wrapper.find('h2').text()).toBe('Create Your Story!');

    // Check for form elements by label or type
    expect(wrapper.find('label[for="mainCharacter"]').exists()).toBe(true);
    expect(wrapper.find('select#mainCharacter').exists()).toBe(true);

    expect(wrapper.find('label[for="storyTheme"]').exists()).toBe(true);
    expect(wrapper.find('input#storyTheme').exists()).toBe(true);

    expect(wrapper.find('button[type="submit"]').exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').text()).toBe('Make My Story!');
  });

  it('fetches characters on mount if not already loaded', async () => {
    const storyStore = useStoryStore();
    // Spy on fetchCharacters action
    const fetchCharactersSpy = vi.spyOn(storyStore, 'fetchCharacters');

    mount(StoryPicker, {
      global: {
        plugins: [pinia, router],
      },
    });

    expect(fetchCharactersSpy).toHaveBeenCalledTimes(1);
  });

  it('populates main character select options from store', async () => {
    const storyStore = useStoryStore();
    storyStore.characters = [ // Manually set characters in the store for this test
      { id: 1, name: 'Ellie', emoji: '🐘' },
      { id: 2, name: 'Leo', emoji: '🦁' },
    ];

    const wrapper = mount(StoryPicker, {
      global: {
        plugins: [pinia, router],
      },
    });

    // Wait for Vue to update the DOM after characters are set
    await wrapper.vm.$nextTick();

    const options = wrapper.findAll('select#mainCharacter option');
    // Expected: "Please select one" + 2 characters
    expect(options.length).toBe(3);
    expect(options[1].text()).toBe('🐘 Ellie');
    expect(options[1].element.value).toBe('1');
    expect(options[2].text()).toBe('🦁 Leo');
    expect(options[2].element.value).toBe('2');
  });

  it('disables submit button if main character is not selected', async () => {
    const wrapper = mount(StoryPicker, {
      global: {
        plugins: [pinia, router],
      },
    });

    const submitButton = wrapper.find('button[type="submit"]');
    expect(submitButton.attributes('disabled')).toBeDefined();

    // Select a character
    await wrapper.find('select#mainCharacter').setValue('1'); // Assuming a character with id 1 exists or is mocked
     // Need to ensure store.characters has an item with id 1 for this to pass if component logic relies on it
    storyStore.characters = [{ id: 1, name: 'TestChar', emoji: 'TC' }];
    await wrapper.vm.$nextTick();
    await wrapper.find('select#mainCharacter').setValue('1');


    // Re-check button (it might still be disabled if store.isLoading is true by default, or other conditions)
    // For this specific test, let's assume isLoading is false and a character is selected.
    // The button's disabled state is `storyStore.isLoading || !selectedMainCharacterId`
    // So if selectedMainCharacterId is set, and isLoading is false, it should be enabled.

    // storyStore.isLoading = false; // Ensure isLoading is false
    // await wrapper.vm.$nextTick();
    // This direct mutation might not be ideal. Better to check component's internal selectedMainCharacterId ref.
    // The component sets selectedMainCharacterId.value when the select changes.

    // After setting the value, the component's internal `selectedMainCharacterId` ref should update.
    // The button's :disabled attribute depends on `!selectedMainCharacterId` (the ref, not store directly for this part)
    // and `storyStore.isLoading`.

    // Let's ensure storyStore.isLoading is false
    const storyStore = useStoryStore();
    storyStore.isLoading = false;
    await wrapper.vm.$nextTick(); // Allow Vue to react to store change

    expect(submitButton.attributes('disabled')).toBeUndefined(); // Should be enabled
  });

  it('calls generateStory action on form submit with correct parameters', async () => {
    const storyStore = useStoryStore();
    storyStore.characters = [ // Provide characters for selection
      { id: 1, name: 'Ellie', emoji: '🐘' },
      { id: 2, name: 'Leo', emoji: '🦁' },
      { id: 3, name: 'Tilly', emoji: '🐅' },
    ];
    storyStore.isLoading = false; // Ensure not loading initially

    // Spy on the generateStory action
    const generateStorySpy = vi.spyOn(storyStore, 'generateStory').mockResolvedValue({ id: 'story123' });

    // Mock router.push as it's called after successful generation
    const mockRouter = useRouter(); // Get the mocked router instance

    const wrapper = mount(StoryPicker, {
      global: {
        plugins: [pinia, router], // Use the actual router instance here which gets mocked by vi.mock
      },
    });

    // Simulate user input
    await wrapper.find('select#mainCharacter').setValue('1');
    // Simulate selecting supporting characters - this requires clicking the custom checkbox elements
    // For simplicity, let's directly manipulate the component's ref for selectedSupportingCharacterIds
    // This is less ideal than simulating clicks but easier for this specific test.
    // wrapper.vm.selectedSupportingCharacterIds = [2]; // Or trigger click on the divs

    // More robust: find the clickable div and trigger click
    // This requires the divs to be rendered, which they are if availableCharacters is populated.
    const supportCharDivs = wrapper.findAllComponents({ name: 'div' }).filter(d => d.attributes('key')?.startsWith('support-'));
    if (supportCharDivs.length > 1) { // Ensure there's a character to click that isn't main
        // Click the one for character id 2 (Leo)
        const leoDiv = supportCharDivs.find(div => div.attributes('key') === 'support-2');
        if (leoDiv) await leoDiv.trigger('click');
    }

    await wrapper.find('input#storyTheme').setValue('A Grand Test');

    // Submit the form
    await wrapper.find('form').trigger('submit.prevent');

    expect(generateStorySpy).toHaveBeenCalledTimes(1);
    expect(generateStorySpy).toHaveBeenCalledWith({
      main_character_id: '1', // select value is string
      supporting_character_ids: [2], // Assuming Leo (id 2) was clicked
      story_theme: 'A Grand Test',
    });

    // Check if router.push was called (requires async completion of generateStory)
    await wrapper.vm.$nextTick(); // Wait for promises from generateStory to resolve
    await wrapper.vm.$nextTick(); // Additional tick might be needed

    expect(mockRouter.push).toHaveBeenCalledWith({ name: 'StoryRead', params: { id: 'story123' } });
  });

  // Add more tests:
  // - Supporting character selection logic (max 2, cannot be main character)
  // - Error display when storyStore.error has a value
  // - Loading state display on button when storyStore.isLoading is true
});
