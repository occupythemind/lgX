from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Topic, Entry

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Topic):
            return obj.owner_id == request.user.current_profile_id
        elif isinstance(obj, Entry):
            # let's see if the cause of vuln (1.) is here
            print(obj.topic.owner_id)
            return obj.topic.owner_id == request.user.current_profile_id
