# Assist.IA - AI Assistant API

This is a FastAPI-based application that provides an interface to interact with Groq Models. The application allows you to send questions and receive AI-generated responses, with built-in authentication support.

## Use Cases

### 1. Personal Professional Agent
- Automated CV presentation and professional profile management
- Dynamic responses about professional experience and skills
- Customized presentations for different job opportunities
- Real-time updates of professional achievements and projects

### 2. Document Analysis and RAG (Retrieval Augmented Generation)
- PDF document processing and information extraction
- Intelligent document search and retrieval
- Context-aware responses based on document content
- Knowledge base creation from multiple documents

### 3. Micro Tasks and Consulting
- Quick technical consultations
- Code review and suggestions
- Technical documentation generation
- Problem-solving assistance
- Best practices recommendations

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
   - Configure the following environment variables in your `.env` file:
     ```
     GROQ_API_KEY=your_groq_api_key
     DEFAULT_INSTRUCTIONS=your_default_instructions
     ENABLE_AUTH=true
     TOKEN_SECRET=your_token_secret
     CHROMA_PATH=./chroma_db
     LOCAL_DATA_PATH=./data
     ```

## Running the Application

1. Start the server:
```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## API Usage

### Authentication

The API supports authentication. When `ENABLE_AUTH` is set to `true`, you need to include a valid token in your requests.

### Endpoints

#### 1. Ask Question (POST /api/ask)
Send questions to the AI assistant using this endpoint.

##### Request Format:
```json
{
    "instructions": "Optional custom instructions for the AI",
    "question": "Your question here"
}
```

##### Example using curl:
```bash
curl -X POST "http://localhost:8000/api/ask" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your_token_here" \
     -d '{"question": "What is artificial intelligence?"}'
```

##### Response Format:
```json
{
    "response": "AI-generated response here"
}
```

#### 2. Document Processing (POST /api/process-document)
Upload and process PDF documents for RAG implementation.

##### Request Format:
```json
{
    "document_path": "path/to/your/document.pdf",
    "instructions": "Optional processing instructions"
}
```

##### Example using curl:
```bash
curl -X POST "http://localhost:8000/api/process-document" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your_token_here" \
     -d '{"document_path": "./data/resume.pdf"}'
```

#### 3. Professional Profile (GET /api/profile)
Retrieve professional profile information.

##### Example using curl:
```bash
curl -X GET "http://localhost:8000/api/profile" \
     -H "Authorization: Bearer your_token_here"
```

## Features

- Integration with GROQ Cloud
- Customizable instructions for each request
- FastAPI-powered REST API
- CORS enabled for cross-origin requests
- Environment variable configuration
- Error handling for API requests
- Authentication support
- Vector database integration with ChromaDB
- Local data storage support
- PDF document processing
- RAG implementation for document-based responses
- Professional profile management

## Requirements

- Python 3.7+
- Groq API
- Dependencies listed in requirements.txt

## Error Handling

The API will return an error message if:
- The GROQ API key is invalid or missing
- There's an error in generating the response
- The request format is incorrect
- Authentication fails (when enabled)
- Document processing fails
- Invalid document format

## Security Notes

- Keep your API keys and token secret secure and never commit them to version control
- Use environment variables for sensitive information
- The API is configured to accept requests from any origin (CORS) - modify this in production
- When authentication is enabled, ensure proper token management
- Implement proper access control for document processing
- Regularly update dependencies for security patches

