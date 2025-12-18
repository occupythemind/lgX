from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Topic, Entry

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Topic):
            return obj.owner_id == request.user.current_profile
        elif isinstance(obj, Entry):
            return obj.topic.owner_id == request.user.current_profile
