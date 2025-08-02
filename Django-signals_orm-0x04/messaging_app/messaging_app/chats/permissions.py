# messaging_app/chats/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrParticipant(BasePermission):
    """
    Allows access only if the user is the sender, recipient, or a participant.
    """

    def has_object_permission(self, request, view, obj):
        # If the object is a message
        if hasattr(obj, 'sender') and hasattr(obj, 'recipient'):
            return obj.sender == request.user or obj.recipient == request.user

        # If the object is a conversation (e.g., has participants)
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        return False

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to authenticated users who are participants in the conversation.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated for all requests
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For Message objects
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        # If the object itself is a Conversation
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        return False