# Context-Aware Chatbot

A beginner-friendly AI learning assistant built using FastAPI and Google's Gemini API. The chatbot maintains conversation history so that it can answer follow-up questions using earlier messages.

## Features

- **LLM integration:** Uses the Gemini API to generate responses.
- **Multi-turn conversations:** Maintains separate conversation histories using conversation IDs.
- **Context management:** Keeps the most recent 10 history messages to limit the context sent to the model.
- **Custom system prompt:** Guides the assistant to explain concepts in simple language with examples.
- **Input validation:** Rejects empty messages and empty conversation IDs.
- **Error handling:** Returns meaningful HTTP errors when requests fail.
- **Web interface:** Provides a simple chat interface using HTML, CSS, and JavaScript.
- **Environment variables:** Stores the API key and model configuration outside the source code.

## Technologies Used

- Python
- FastAPI
- Google Gemini API (`google-genai`)
- Pydantic
- HTML, CSS, and JavaScript
- Uvicorn
- python-dotenv

## Project Structure

```text
context_aware_chatbot/
├── backend/
│   └── main.py
├── frontend/
│   └── index.html
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

The `.env` file is for local configuration and must not be uploaded to GitHub.

## Prerequisites

- Python installed on your computer
- A Google Gemini API key from Google AI Studio
- Internet access to call the Gemini API

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Rubida6/context-aware-chatbot.git
cd context_aware_chatbot
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the URL of your published repository.

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project's root directory:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Replace `your_gemini_api_key` with your own API key. Never commit or publish the real key.

### 5. Start the backend

Run this command from the project root:

```bash
python -m uvicorn backend.main:app --reload
```

### 6. Open the chatbot

Visit:

http://127.0.0.1:8000/ui

The API documentation is available at:

http://127.0.0.1:8000/docs

## How It Works

1. The user enters a message in the web interface.
2. JavaScript sends the message and its conversation ID to the FastAPI `/chat` endpoint.
3. The backend retrieves the previous messages associated with that conversation ID.
4. The backend sends the conversation history, the new message, and the system instructions to Gemini.
5. Gemini generates a response.
6. The backend saves the new user message and assistant response in the conversation history.
7. The response is returned to the browser and displayed in the chat interface.

## Example Conversation

**User:** My name is Sam.

**Assistant:** Nice to meet you, Sam!

**User:** I am learning Java.

**Assistant:** That's awesome! What part of Java would you like to explore?

**User:** What is my name, and what am I learning?

**Assistant:** Your name is Sam, and you are learning Java!

## Context Management

The application stores conversation history in a Python dictionary, using the conversation ID as the key. It retains the latest 10 history messages for subsequent requests.

This history is stored in memory, so it is cleared when the backend process restarts. A persistent database could be added in a future version.

## Security Notes

- Keep the Gemini API key in `.env`.
- Ensure `.env` is excluded through `.gitignore`.
- Never publish API keys in source code, screenshots, or repository commits.

## Future Improvements

- Persist conversation history in a database.
- Add conversation deletion and reset functionality.
- Improve handling of API rate limits and timeouts.
- Add automated tests for conversation memory and error cases.
- Improve the chat interface for mobile devices.

## Author

Developed as a learning project to explore LLM integration, REST APIs, conversation memory, and frontend-backend communication.
