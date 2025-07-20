
# Create your views here.
from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, render


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """
        Create a conversation with participants from request data.
        """
        conversation = serializer.save()
        participants_ids = self.request.data.get('participants', [])
        conversation.participants.set(participants_ids)
        
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related('sender', 'conversation')
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """
        Save a new message with the sender as the authenticated user (or test user).
        """
        # NOTE: Update this to self.request.user if you enable authentication
        sender = self.request.user if self.request.user.is_authenticated else None
        serializer.save(sender=sender)        