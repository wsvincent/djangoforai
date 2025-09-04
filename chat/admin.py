from django.contrib import admin
from django.db.models import Count  # Import Count from models, not admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("title", "get_message_count", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-updated_at",)

    def get_message_count(self, obj):
        return obj.messages.count()

    get_message_count.short_description = "Messages"
    get_message_count.admin_order_field = "messages__count"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(messages__count=Count("messages"))
        return queryset


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("conversation_title", "sender", "content_preview", "timestamp")
    list_filter = ("is_user", "timestamp", "conversation")
    search_fields = ("content", "conversation__title")
    readonly_fields = ("timestamp",)
    ordering = ("-timestamp",)

    def conversation_title(self, obj):
        return obj.conversation.title

    conversation_title.short_description = "Conversation"
    conversation_title.admin_order_field = "conversation__title"

    def sender(self, obj):
        return "User" if obj.is_user else "Gemma 3 4B"

    sender.short_description = "Sender"
    sender.admin_order_field = "is_user"

    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content

    content_preview.short_description = "Content"

    # Custom fieldsets for better organization
    fieldsets = (
        (None, {"fields": ("conversation", "is_user", "content")}),
        ("Timestamps", {"fields": ("timestamp",), "classes": ("collapse",)}),
    )
