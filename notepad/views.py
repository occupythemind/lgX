from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from .serializers import TopicSerializer, EntrySerializer
from .models import Topic, Entry

class TopicAPIView(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Topic.objects.filter(owner=self.request.user.current_profile)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.current_profile)

class EntryAPIView(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if self.kwargs.get('topic_pk', ''):
            return Entry.objects.filter(topic__owner=self.request.user.current_profile, topic_id=self.kwargs.get('topic_pk', ''))
        return Entry.objects.filter(topic__owner=self.request.user.current_profile)

    # (1.) vulnerable to IDOR by using POST to add entries to a nested endpoint.
    def perform_create(self, serializer):
        if self.kwargs.get('topic_pk', ''):
            serializer.save(topic=Topic.objects.get(pk=self.kwargs.get('topic_pk', '')))
        else:
            raise ValidationError('This endpoint does not appreciate POST requests, use /api/topics/{pk}/entries rather.')