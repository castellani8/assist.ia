from langchain_groq import ChatGroq
from groq import Groq
import os


def get_groq_response(
        sys_msg, 
        usr_msg,
        history=[],
        model_name='llama3-8b-8192',
        temperature=0.2,
        max_tokens=1024
    ) -> str:
    groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

    try:
        response = groq.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": usr_msg}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(e)
        return "An error occurred while generating the response."
