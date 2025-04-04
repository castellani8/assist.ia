# Assist.IA - AI Assistant API

This is a FastAPI-based application that provides an interface to interact with Google's Gemini AI model. The application allows you to send questions and receive AI-generated responses.

## Installation Instructions

1. Create a Python virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- On macOS/Linux:
```bash
source venv/bin/activate
```
- On Windows:
```bash
.\venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy the `.env.example` file to `.env`
   - Add your Google API key to the `.env` file:
     ```
     GOOGLE_API_KEY=your_api_key_here
     DEFAULT_INSTRUCTIONS=your_default_instructions_here
     ```

## Running the Application

1. Start the server:
```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## API Usage

### Endpoint: POST /api/ask

Send questions to the AI assistant using this endpoint.

#### Request Format:
```json
{
    "instructions": "Optional custom instructions for the AI",
    "question": "Your question here"
}
```

#### Example using curl:
```bash
curl -X POST "http://localhost:8000/api/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is artificial intelligence?"}'
```

#### Response Format:
```json
{
    "response": "AI-generated response here"
}
```

## Features

- Integration with Google's Gemini AI model
- Customizable instructions for each request
- FastAPI-powered REST API
- CORS enabled for cross-origin requests
- Environment variable configuration
- Error handling for API requests

## Requirements

- Python 3.7+
- Google API key for Gemini
- Dependencies listed in requirements.txt

## Error Handling

The API will return an error message if:
- The Google API key is invalid or missing
- There's an error in generating the response
- The request format is incorrect

## Security Notes

- Keep your API key secure and never commit it to version control
- Use environment variables for sensitive information
- The API is configured to accept requests from any origin (CORS) - modify this in production

