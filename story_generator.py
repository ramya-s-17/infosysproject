"""Advanced Interactive Story Generator using Groq API."""
import os, json
from groq import Groq
from typing import Dict, Any

class StoryGenerator:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found")
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"

    def generate_story(self, prompt: str, style: str = "epic", length: int = 5) -> Dict[str, Any]:
        try:
            system_prompt = f"""You are a master storyteller. Generate a rich, immersive story in '{style}' style.
Return ONLY valid JSON:
{{
  "title": "Compelling story title",
  "genre": "fantasy|sci-fi|adventure|mystery|romance|horror",
  "theme": "theme keyword",
  "emoji": "single emoji",
  "tagline": "one punchy tagline under 10 words",
  "world": "brief world description 1 sentence",
  "scenes": [
    {{
      "id": 1,
      "title": "Scene title",
      "text": "3-4 vivid sentence scene description with sensory details",
      "mood": "happy|sad|tense|mysterious|epic|peaceful|dramatic|thrilling",
      "location": "specific location name",
      "weather": "sunny|stormy|foggy|night|dawn|dusk|snowy",
      "character": "main character in this scene",
      "action": "key action verb",
      "dialogue": "one memorable quote from this scene",
      "stats": {{"Power": number, "Danger": number, "Mystery": number}},
      "color_theme": "hex color like #ff8c00"
    }}
  ],
  "characters": [
    {{"name": "name", "role": "role", "emoji": "emoji", "trait": "key personality trait", "backstory": "one sentence backstory"}}
  ],
  "timeline": [
    {{"year": "time period", "event": "event", "significance": "why it matters"}}
  ],
  "world_facts": [
    {{"fact": "interesting world fact", "icon": "emoji"}}
  ],
  "moral": "deep moral lesson",
  "sequel_hook": "one sentence teaser for what happens next"
}}
Generate exactly {length} scenes. Stats are 0-100. Make it vivid and emotionally engaging."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Create a {style} story about: {prompt}"}
                ],
                temperature=0.85,
                max_tokens=3000
            )
            content = response.choices[0].message.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            story_data = json.loads(content)
            return {"success": True, "story": story_data}
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Parse error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def continue_story(self, story: dict, direction: str) -> Dict[str, Any]:
        """Generate a continuation scene for the story."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a storyteller. Return ONLY valid JSON for a new scene object matching the existing story structure with fields: id, title, text, mood, location, weather, character, action, dialogue, stats, color_theme."},
                    {"role": "user", "content": f"Story: {story['title']}. Continue with: {direction}. Return one new scene JSON object only."}
                ],
                temperature=0.9,
                max_tokens=600
            )
            content = response.choices[0].message.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            new_scene = json.loads(content)
            return {"success": True, "scene": new_scene}
        except Exception as e:
            return {"success": False, "error": str(e)}
