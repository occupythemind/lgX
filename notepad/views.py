from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwner
from .serializers import TopicSerializer, EntrySerializer
from .models import Topic, Entry

class TopicAPIView(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Topic.objects.filter(owner=self.request.user.current_profile_id)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.current_profile_id)

class EntryAPIView(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if self.kwargs.get('topic_pk', ''):
            topic = Topic.objects.get(pk=self.kwargs.get('topic_pk', ''))
            if self.request.user.current_profile_id != topic.owner.id:
                raise NotFound({'detail':'No Topic matches the given query.'})
            return Entry.objects.filter(topic__owner=self.request.user.current_profile_id, topic_id=self.kwargs.get('topic_pk', ''))
        return Entry.objects.filter(topic__owner=self.request.user.current_profile_id)

    # (1.) vulnerable to IDOR by using POST to add entries to a nested endpoint. Now, I suspect that
    # PATCH, PUT & DELETE requests may also work. Later on, I may use burp. to test, the start correcting.
    def perform_create(self, serializer):
        if self.kwargs.get('topic_pk', ''):
            topic = Topic.objects.get(pk=self.kwargs.get('topic_pk', ''))
            if self.request.user.current_profile_id != topic.owner.id:
                raise NotFound({'detail':'No Topic matches the given query.'})
            serializer.save(topic=topic)
        else:
            raise ValidationError('This endpoint does not appreciate POST requests, use /api/topics/{pk}/entries rather.')