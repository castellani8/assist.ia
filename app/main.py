from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)

prompt = "How are you?"
response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents=prompt)

print(response.text)