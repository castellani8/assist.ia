from google import genai
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_gemini_response(
        prompt: str, 
        model: str = "gemini-2.0-flash-lite"
        ) -> str:
    client = genai.Client(api_key=GOOGLE_API_KEY)

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt)
        return response.text
    except Exception as e:
        print(e)
        return "An error occurred while generating the response."
