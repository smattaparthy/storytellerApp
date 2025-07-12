import time
import random
from typing import List, Dict, Any, Tuple

# from app.core.config import settings # If API key needed for actual service
# from app.models.character import Character as CharacterModel # If fetching character details

class GeminiStoryService:
    """
    Mock service for generating stories and image prompts, simulating Google Gemini Pro.
    """
    def __init__(self):
        # In a real service, you'd initialize the Gemini client here
        # e.g., self.client = generativeai.GenerativeModel(settings.GEMINI_MODEL)
        print("MockGeminiStoryService initialized.")

    async def generate_story_and_prompts(
        self,
        main_character_name: str,
        supporting_character_names: List[str],
        theme: str,
        story_length_words: int = 250 # Approx.
    ) -> Dict[str, Any]:
        """
        Generates a story, title, moral lessons, and image prompts.
        Simulates API call latency.
        """
        print(f"Mock AI: Generating story for {main_character_name} with friends {supporting_character_names} on theme '{theme}'.")
        await asyncio.sleep(random.uniform(0.5, 1.5)) # Simulate network latency

        story_templates = [
            f"{main_character_name} went on a thrilling {theme.lower()} adventure in the Whispering Woods. Along the way, {main_character_name} met {', '.join(supporting_character_names) if supporting_character_names else 'some new friends'}. They discovered a hidden waterfall and learned that working together makes any challenge fun! The biggest lesson was that true treasure is friendship.",
            f"One sunny morning, {main_character_name} decided to build the tallest block tower ever. It was a real {theme.lower()}! {f'{supporting_character_names[0]} helped by finding colorful blocks.' if supporting_character_names else 'It was tricky work.'} After a few tumbles, they finally did it! {main_character_name} learned that patience and trying again leads to success, and it's always good to ask for help.",
            f"In the magical land of Sparkletoot, {main_character_name} was known for being curious. One day, a mysterious map appeared, promising a {theme.lower()}. {f'With brave companions like {", ".join(supporting_character_names)},' if supporting_character_names else ""} {main_character_name} followed the clues. They found not gold, but a lost baby bird, which they kindly returned to its nest. The moral of the story: kindness is the greatest adventure."
        ]

        selected_story = random.choice(story_templates)

        # Simple word count based split for pagination (very naive)
        words = selected_story.split()
        num_pages = 2 # Fixed for now as per spec MAX_IMAGES_PER_STORY=2 implies 2-3 pages
        words_per_page = len(words) // num_pages

        paginated_content = []
        for i in range(num_pages):
            start_index = i * words_per_page
            end_index = (i + 1) * words_per_page if i < num_pages - 1 else len(words)
            page_text = " ".join(words[start_index:end_index])
            paginated_content.append({
                "page_num": i + 1,
                "text": page_text,
                # Placeholder for image linking, PageFormatter will handle this
                "image_placeholder_id": f"img_placeholder_{i+1}" if i < settings.MAX_IMAGES_PER_STORY else None
            })

        image_prompts = [
            f"A child-friendly, vibrant illustration of {main_character_name} in a {theme.lower()} setting, happy and adventurous.",
            f"Cute cartoon of {main_character_name} {'and ' + supporting_character_names[0] if supporting_character_names else ''} discovering something exciting, bright colors, storybook style."
        ][:settings.MAX_IMAGES_PER_STORY] # Max 2 image prompts

        response = {
            "title": f"The Grand {theme} of {main_character_name}",
            "full_content_raw": selected_story, # The full, unpaginated story text
            "paginated_content_stubs": paginated_content, # Stubs for PageFormatter
            "moral_lessons": [
                "Friendship is important.",
                "Teamwork makes dreams work.",
                "Be kind to others."
            ],
            "image_prompts": image_prompts,
            "theme_echo": theme # Echoing the theme for consistency
        }

        print(f"Mock AI: Story generation complete for {main_character_name}.")
        return response

# Need to import asyncio and settings for the above code
import asyncio
from app.core.config import settings # Assuming settings are used for MAX_IMAGES_PER_STORY

# Example usage (if you were to run this file directly for testing)
async def main():
    service = GeminiStoryService()
    story_data = await service.generate_story_and_prompts(
        main_character_name="Ellie the Elephant",
        supporting_character_names=["Leo the Lion", "Tilly the Tiger"],
        theme="Jungle Exploration"
    )
    print("\n--- Generated Story Data (Mock) ---")
    import json
    print(json.dumps(story_data, indent=2))
    print("--- End of Story Data ---")

if __name__ == "__main__":
    asyncio.run(main())
