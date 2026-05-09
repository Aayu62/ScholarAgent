import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def generate_response(query, context):
    if not client:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    prompt = f"""
    You are ScholarAgent, an AI research assistant.

    Answer the user's question ONLY using the provided context.

    If the answer is not present in the context, say:
    "The uploaded documents do not contain enough information."

    Context:
    {context}

    User Question:
    {query}

    Answer:
    """

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
    except Exception as exc:
        raise RuntimeError(f"Gemini API request failed: {exc}") from exc

    return response.text
