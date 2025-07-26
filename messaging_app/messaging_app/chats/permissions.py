# messaging_app/chats/permissions.py

from rest_framework.permissions import BasePermission

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
