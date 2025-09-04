"""Custom exceptions for the chat application"""


class ChatException(Exception):
    """Base exception for chat-related errors"""
    pass


class OllamaConnectionError(ChatException):
    """Raised when unable to connect to Ollama API"""
    pass


class OllamaResponseError(ChatException):
    """Raised when Ollama returns an invalid response"""
    pass


class MessageValidationError(ChatException):
    """Raised when message validation fails"""
    pass


class ConversationNotFoundError(ChatException):
    """Raised when a conversation is not found"""
    pass


class StreamingError(ChatException):
    """Raised when SSE streaming encounters an error"""
    pass