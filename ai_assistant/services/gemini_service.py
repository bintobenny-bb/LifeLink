from ai_assistant.services.inventory_service import get_available_inventory
from ai_assistant.prompts.system_prompt import SYSTEM_PROMPT
import time
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
    Generate a LifeLink AI response using Gemini
    with live blood inventory database context.
    """

    # Fetch live inventory from database
    inventory_data = get_available_inventory()

    # Convert inventory records into readable context
    inventory_context = (
        "\n".join(
            [
                f"- Blood Group: {item['blood_group']} | "
                f"Component: {item['component']} | "
                f"Units: {item['units_available']} | "
                f"Hospital: {item['hospital__hospital_name']}"
                for item in inventory_data
            ]
        )
        if inventory_data
        else "No currently available blood inventory records found."
    )

    # Build Gemini prompt
    full_prompt = f"""
{SYSTEM_PROMPT}

LIVE BLOOD INVENTORY DATA:
{inventory_context}

INSTRUCTIONS FOR INVENTORY QUESTIONS:
- Use the inventory data above when answering questions about blood availability.
- Never invent stock, blood groups, units, hospitals, or availability.
- If the requested blood group or component is not listed, say it is not currently listed in the available inventory.
- Mention the hospital name and available units when relevant.
- Treat this inventory as the current database snapshot.
- Do not claim that a blood request has been fulfilled or a donor has been found.

USER MESSAGE:
{prompt}
"""

    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=full_prompt,
            )

            if response.text:
                return response.text.strip()

            return "I'm sorry, I couldn't generate a response."

        except Exception as e:
            error_message = str(e)

            if ("503" in error_message or "429" in error_message) and attempt < max_retries - 1:
                wait_time = 2 ** (attempt + 1)
                print(
                    f"Gemini temporarily unavailable. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            print(f"Gemini API Error: {e}")
            return "I'm temporarily unable to respond. Please try again later."

    return "I'm temporarily unable to respond. Please try again later."
