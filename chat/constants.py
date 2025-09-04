"""Constants and configuration for the chat application"""

# Ollama API Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_CHAT_ENDPOINT = f"{OLLAMA_BASE_URL}/api/chat"
OLLAMA_MODEL = "gemma3:4b"
OLLAMA_TIMEOUT = 60.0  # seconds
OLLAMA_STREAM_TIMEOUT = 60.0

# Message Configuration
MAX_MESSAGE_LENGTH = 10000
CONVERSATION_CONTEXT_LIMIT = 10  # Number of previous messages to include
TITLE_TRUNCATE_LENGTH = 50

# UI Configuration
RECENT_CONVERSATIONS_LIMIT = 5
MESSAGE_PREVIEW_LENGTH = 100

# Response Messages
ERROR_MESSAGES = {
    "EMPTY_MESSAGE": "Message cannot be empty",
    "MESSAGE_TOO_LONG": f"Message is too long (max {MAX_MESSAGE_LENGTH} characters)",
    "OLLAMA_CONNECTION": "Could not connect to the local Gemma model",
    "OLLAMA_ERROR": "Sorry, I'm having trouble connecting to Gemma 3 4B.",
    "NO_RESPONSE": "No response received from the model",
    "INVALID_JSON": "Invalid JSON in request",
}

# Model Display Names
AI_DISPLAY_NAME = "Gemma 3 4B"
AI_AVATAR_TEXT = "G3"