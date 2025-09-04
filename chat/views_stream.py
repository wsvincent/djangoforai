import httpx
import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Conversation, Message
from .views import render_markdown
from .services import ConversationService
from .constants import ERROR_MESSAGES, OLLAMA_CHAT_ENDPOINT, OLLAMA_MODEL


@method_decorator(csrf_exempt, name="dispatch")
class StreamChatView(SingleObjectMixin, View):
    """SSE endpoint for streaming AI responses"""
    
    model = Conversation
    pk_url_kwarg = "conversation_id"
    
    def get(self, request, *args, **kwargs):
        """Stream AI response using Server-Sent Events"""
        message_id = request.GET.get("message_id")
        if not message_id:
            return HttpResponse("Missing message_id", status=400)
        
        self.object = self.get_object()
        conversation = self.object
        user_message = get_object_or_404(
            Message, id=message_id, conversation=conversation, is_user=True
        )

        # Build conversation context
        messages = list(conversation.messages.all().order_by("timestamp"))
        ollama_messages = []
        for msg in messages[-10:]:
            role = "user" if msg.is_user else "assistant"
            ollama_messages.append({"role": role, "content": msg.content})

        def generate():
            """Generator function for SSE streaming"""
            full_response = ""
            
            try:
                # Use synchronous httpx client with stream
                with httpx.Client(timeout=60.0) as client:
                    with client.stream(
                        "POST",
                        OLLAMA_CHAT_ENDPOINT,
                        json={
                            "model": OLLAMA_MODEL,
                            "messages": ollama_messages,
                            "stream": True,
                        },
                    ) as response:
                        for line in response.iter_lines():
                            if line:
                                try:
                                    data = json.loads(line)
                                    if "message" in data and "content" in data["message"]:
                                        token = data["message"]["content"]
                                        full_response += token
                                        yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
                                except json.JSONDecodeError:
                                    continue
                                except Exception as e:
                                    yield f"data: {json.dumps({'type': 'error', 'content': f'Parse error: {str(e)}'})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'content': f'Connection error: {str(e)}'})}\n\n"
                return

            # Save the complete message if we got a response
            if full_response:
                ai_message = ConversationService.add_ai_message(
                    conversation, full_response
                )
                # Send completion signal
                yield f"data: {json.dumps({'type': 'done', 'timestamp': ai_message.timestamp.strftime('%I:%M %p')})}\n\n"
            else:
                yield f"data: {json.dumps({'type': 'error', 'content': ERROR_MESSAGES['NO_RESPONSE']})}\n\n"

        response = StreamingHttpResponse(
            generate(), content_type="text/event-stream"
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response


@method_decorator(csrf_exempt, name="dispatch") 
class RenderMarkdownView(View):
    """API endpoint to render markdown to HTML"""
    
    def post(self, request, conversation_id):
        """Render markdown content to HTML"""
        try:
            data = json.loads(request.body)
            content = data.get("content", "")
            rendered = render_markdown(content)
            return HttpResponse(rendered)
        except json.JSONDecodeError:
            return JsonResponse({"error": ERROR_MESSAGES["INVALID_JSON"]}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)