from services.gemini import get_gemini_response
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    instructions = os.getenv("INSTRUCTIONS")
    print(instructions)
    prompt = "who created you?"
    print(get_gemini_response(instructions+"\n\n"+prompt))

if __name__ == "__main__":
    main()