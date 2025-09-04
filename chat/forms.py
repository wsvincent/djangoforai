from django import forms
from django.core.exceptions import ValidationError
from .models import Message


class MessageForm(forms.ModelForm):
    """Form for creating new messages in a conversation"""
    
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control border-0 bg-light',
                'placeholder': 'Message Gemma 3 4B...',
                'autocomplete': 'off',
                'required': True,
            })
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise ValidationError('Message cannot be empty')
        if len(content) > 10000:
            raise ValidationError('Message is too long (max 10,000 characters)')
        return content


class ConversationStartForm(forms.Form):
    """Form for starting a new conversation from the homepage"""
    
    message = forms.CharField(
        max_length=10000,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg border-0',
            'placeholder': 'Ask Gemma 3 4B anything...',
            'autocomplete': 'off',
        })
    )
    
    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if not message:
            raise ValidationError('Message cannot be empty')
        return message