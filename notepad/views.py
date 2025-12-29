from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .permissions import IsOwner
from .serializers import TopicSerializer, EntrySerializer
from .models import Topic, Entry

class TopicAPIView(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_fields = {
        'created': ['gte', 'lte', 'exact'],
        'title': ['icontains'],
        'status': ['exact'],
    }
    search_fields = ['title']
    ordering_fields = ['created', 'title', 'status']
    ordering = ['-created']

    def get_queryset(self):
        return Topic.objects.filter(owner=self.request.user.current_profile_id)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.current_profile_id)
    
    def perform_destroy(self, instance):
        if instance.status == 'TRASH':
            return super().perform_destroy(instance)
        else:
            instance.status = 'TRASH'
            instance.save()

class EntryAPIView(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_fields = {
        'created': ['gte', 'lte', 'exact'],
        'text': ['icontains'],
        'status': ['exact'],
    }
    search_fields = ['text']
    ordering_fields = ['created', 'text', 'status']
    ordering = ['-created']

    def get_queryset(self):
        if self.kwargs.get('topic_pk', ''):
            topic = Topic.objects.get(pk=self.kwargs.get('topic_pk', ''))
            if self.request.user.current_profile_id != topic.owner.id:
                raise NotFound({'detail':'No Topic matches the given query.'})
            return Entry.objects.filter(topic__owner=self.request.user.current_profile_id, topic_id=self.kwargs.get('topic_pk', ''))
        return Entry.objects.filter(topic__owner=self.request.user.current_profile_id)

    def perform_create(self, serializer):
        if self.kwargs.get('topic_pk', ''):
            topic = Topic.objects.get(pk=self.kwargs.get('topic_pk', ''))
            if self.request.user.current_profile_id != topic.owner.id:
                raise NotFound({'detail':'No Topic matches the given query.'})
            serializer.save(topic=topic)
        else:
            raise ValidationError(settings.MSG_ERROR_METHOD_REFER % ('POST', '/api/topics/{pk}/entries/'))
        
    def perform_destroy(self, instance):
        if instance.status == 'TRASH':
            return super().perform_destroy(instance)
        else:
            instance.status = 'TRASH'
            instance.save()