from rest_framework import serializers
from account.models import Profile
from .models import Topic, Entry

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'
        read_only_fields = ['id', 'topic']


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = '__all__'
        read_only_fields = ['id', 'owner']

    def create(self, validated_data):
        validated_data['owner'] = Profile.objects.get(id=self.context['request'].user.current_profile_id)
        return super().create(validated_data)