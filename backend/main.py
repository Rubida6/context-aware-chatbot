import os
from pathlib import Path
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

load_dotenv()

app = FastAPI(title="Context-Aware Chatbot")

BASE_DIR = Path(__file__).resolve().parent.parent

@app.get("/ui")
def chat_ui():
    return FileResponse(BASE_DIR / "frontend" / "index.html")

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

SYSTEM_PROMPT = """
You are a friendly learning assistant.

Rules:
1. Use simple language suitable for beginners.
2. Answer the user's actual question directly.
3. Use previous messages to remember relevant conversation details.
4. If the user asks about their name or what they are learning,
   answer using the conversation history.
5. Keep simple answers short.
6. For programming concepts, give a clear explanation
   and a small example when useful.
7. If a question is unclear, ask a short clarifying question.
"""


class ChatRequest(BaseModel):
    conversation_id: str
    message: str

conversation_histories = {}

MAX_HISTORY_MESSAGES = 10

@app.get("/")
def home():
    return {"message": "Context-Aware Chatbot API is running"}


@app.post("/chat")
def chat(request: ChatRequest):
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key is not configured."
        )

    if not request.conversation_id.strip():
        raise HTTPException(
            status_code=400,
            detail="Conversation ID cannot be empty."
        )

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:
        client = genai.Client(api_key=API_KEY)

        # Get the history for this conversation.
        history = conversation_histories.get(
            request.conversation_id, []
        )

        # Include previous messages and the new question.
        contents = history + [
            {
                "role": "user",
                "parts": [{"text": request.message}]
            }
        ]

        # Ask Gemini using the conversation context.
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            ),
        )

        if not response.text:
            raise HTTPException(
                status_code=502,
                detail="The AI returned an empty response."
            )

        # Save the new user message and Gemini's reply.
        history.extend([
            {
                "role": "user",
                "parts": [{"text": request.message}]
            },
            {
                "role": "model",
                "parts": [{"text": response.text}]
            }
        ])

        # Keep only the latest 10 messages.
        history = history[-MAX_HISTORY_MESSAGES:]

        # Save the updated history under this conversation ID.
        conversation_histories[request.conversation_id] = history

        return {
            "conversation_id": request.conversation_id,
            "reply": response.text
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Gemini error:", repr(e))

        raise HTTPException(
            status_code=502,
            detail="Gemini API request failed. Check the server terminal."
        )
