from django.db import models
from django.utils import timezone


class ConversationManager(models.Manager):
    """Custom manager for Conversation model"""
    
    def recent(self, limit=5):
        """Get recent conversations"""
        return self.get_queryset().order_by('-updated_at')[:limit]
    
    def with_messages(self):
        """Get conversations with prefetched messages"""
        return self.get_queryset().prefetch_related('messages')
    
    def create_with_message(self, message_content):
        """Create a conversation with an initial message"""
        title = (
            message_content[:50] + "..."
            if len(message_content) > 50
            else message_content
        )
        conversation = self.create(title=title)
        conversation.messages.create(content=message_content, is_user=True)
        return conversation


class Conversation(models.Model):
    title = models.CharField(max_length=200, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = ConversationManager()
    
    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=['-updated_at']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def message_count(self):
        """Get the total number of messages in this conversation"""
        return self.messages.count()
    
    @property
    def last_message(self):
        """Get the most recent message in this conversation"""
        return self.messages.last()
    
    def get_context_messages(self, limit=10):
        """Get recent messages for context"""
        return list(self.messages.all()[:limit])


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    content = models.TextField()
    is_user = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{'User' if self.is_user else 'AI'}: {self.content[:50]}..."
    
    @property
    def role(self):
        """Get the role for Ollama API"""
        return "user" if self.is_user else "assistant"
    
    @property
    def truncated_content(self):
        """Get truncated content for display"""
        return (
            self.content[:100] + "..."
            if len(self.content) > 100
            else self.content
        )
