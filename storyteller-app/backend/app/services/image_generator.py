import asyncio
import random
import base64
from typing import List, Dict

# from app.core.config import settings # If API key needed for actual service

class ImagenService:
    """
    Mock service for generating images, simulating Google Imagen.
    """
    def __init__(self):
        # In a real service, you'd initialize the Imagen client here
        # e.g., self.client = aiplatform.gapic.PredictionServiceClient(...)
        print("MockImagenService initialized.")

    async def generate_images_base64(self, prompts: List[str]) -> List[str]:
        """
        Generates images based on prompts and returns them as base64 encoded strings.
        Simulates API call latency.
        """
        print(f"Mock AI: Generating {len(prompts)} images for prompts: {prompts}")
        await asyncio.sleep(random.uniform(1.0, 2.0) * len(prompts)) # Simulate network latency

        generated_images_base64 = []
        for i, prompt in enumerate(prompts):
            # Create a dummy placeholder image (e.g., a small colored square)
            # In a real scenario, this would be the actual image data from Imagen.
            # This is a 1x1 red pixel PNG in base64
            dummy_png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
            # More complex placeholder: a 50x50 purple square
            # You can generate such placeholders using an online tool or a simple script
            # For simplicity, we'll use the 1x1 pixel for all.
            # You could also use a library like Pillow to generate a more descriptive placeholder if needed.

            # To make them slightly different, let's pretend they are different images.
            # We can append a comment to the base64 string (which won't affect rendering but makes them unique)
            # Or, more simply, just return the same placeholder for all mock images.

            # For a slightly more "visual" mock, here's a base64 for a 10x10 blue pixel:
            # (Generated from a tool)
            blue_pixel_10x10 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAAXNSR0IArs4c6QAAADNJREFUGJVjZCAS/H9kYGFgYGD4TxwMDExAAkMWYZsRMjA4gKEMn0kBBtAFgwAIAAD//xBJAvf2vc8SAAAAAElFTkSuQmCC"
            # To make it just the base64 part:
            blue_pixel_10x10_data = blue_pixel_10x10.split(",")[1]

            generated_images_base64.append(blue_pixel_10x10_data)
            print(f"Mock AI: Generated mock image for prompt: '{prompt}' (placeholder {i+1})")

        print(f"Mock AI: Image generation complete. Returning {len(generated_images_base64)} base64 strings.")
        return generated_images_base64

# Example usage (if you were to run this file directly for testing)
async def main():
    service = ImagenService()
    prompts = [
        "A happy elephant playing by a river, children's book illustration style.",
        "A brave lion cub standing on a small rock, looking at the sunset, cartoon style."
    ]
    base64_images = await service.generate_images_base64(prompts)

    print("\n--- Generated Image Data (Mock) ---")
    for i, b64_img in enumerate(base64_images):
        print(f"Image {i+1} (base64, first 30 chars): {b64_img[:30]}...")
    print("--- End of Image Data ---")

if __name__ == "__main__":
    asyncio.run(main())
