# Django AI Chat with Ollama and HTMX

A real-time streaming chat application built with Django, HTMX, and Server-Sent Events (SSE) to mimic popular LLMs like ChatGPT, Claude, etc. It integrates with local LLMs via Ollama.

## Features

- 🚀 Real-time streaming responses using Server-Sent Events (SSE)
- 🤖 Local LLM integration via Ollama (Gemma 3 4B)
- 📝 Markdown support with syntax highlighting
- 💬 Conversation history and context management
- 🎨 Clean, responsive UI with HTMX
- 🔄 No heavy JavaScript frameworks required

## Installation

### 1. Install and Configure Ollama

Download and install the [Ollama desktop app](https://ollama.com/) for your platform.

Once installed, pull the Gemma 3 4B model (3.3GB):

```bash
ollama pull gemma3:4b
```

Ensure Ollama is running in the background (it runs on `http://localhost:11434` by default).

### 2. Set Up with uv

[uv](https://docs.astral.sh/uv/) is a fast Python package manager. Install it if you haven't already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then run the project:

```bash
# Install dependencies and run migrations
uv run python manage.py migrate

# Create a superuser to access the admin panel
uv run python manage.py createsuperuser

# Start the development server
uv run python manage.py runserver
```

## Usage

1. Open your browser and navigate to `http://127.0.0.1:8000/`
2. Type a message in the input field
3. Watch as the AI response streams in real-time
4. Previous conversations are saved and accessible from the homepage and the admin at `http://127.0.0.1:8000/admin/`

## Project Structure

```
DjangoForAI/
├── chat/
│   ├── models.py          # Conversation and Message models
│   ├── views.py           # Main view logic using Django CBVs
│   ├── views_stream.py    # SSE streaming implementation
│   ├── urls.py            # URL routing
│   └── migrations/        # Database migrations
├── templates/
│   ├── homepage.html      # Landing page with recent chats
│   └── chat.html          # Chat interface
├── DjangoForAI/
│   ├── settings.py        # Django settings
│   └── urls.py            # Root URL configuration
└── manage.py              # Django management script
```