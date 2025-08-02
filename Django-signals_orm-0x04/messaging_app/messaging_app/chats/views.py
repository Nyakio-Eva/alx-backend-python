
# Create your views here.
from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, render
from rest_framework.permissions import IsAuthenticated
from chats.permissions import IsOwnerOrParticipant
from .permissions import IsParticipantOfConversation
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .pagination import MessagePagination
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    
    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    def perform_create(self, serializer):
        """
        Create a conversation with participants from request data.
        """
        conversation = serializer.save()
        participants_ids = self.request.data.get('participants', [])
        conversation.participants.set(participants_ids)
        
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrParticipant, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
    
    
    
    def get_queryset(self):
        return Message.objects.filter(
            sender=self.request.user
        ) | Message.objects.filter(
            recipient=self.request.user
        )
        
    
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)
    