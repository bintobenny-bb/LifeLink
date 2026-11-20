from ai_assistant.prompts.system_prompt import SYSTEM_PROMPT
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from environment variables.")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"


def generate_response(prompt: str) -> str:
    """
    Generate a LifeLink AI response using Gemini.
    """

    full_prompt = f"""
{SYSTEM_PROMPT}

USER MESSAGE:
{prompt}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt,
        )

        if response.text:
            return response.text.strip()

        return "I'm sorry, I couldn't generate a response."

    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "I'm temporarily unable to respond. Please try again later."
