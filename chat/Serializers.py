from django.contrib.auth.models import User
from .models import MessageModel, UserProfile
from rest_framework import serializers
from django.shortcuts import get_object_or_404

class MessageModelSerializer(serializers.ModelSerializer):
    user= serializers.CharField(source='user.username', read_only=True)
    recipient=serializers.CharField(source='recipient.username')

    def create(self, validated_data):
        user=self.context['request'].user
        recipient = get_object_or_404(
            User, username=validated_data['recipient']['username'])
        msg = MessageModel(recipient=recipient,
                           content=validated_data['content'],
                           user=user)
        msg.save()
        return msg
    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'content')

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class UserProfileSerializer(serializers.ModelSerializer):
    userprofile=serializers.CharField(source='userprofile.username', read_only=True)
    class Meta:
        model=UserProfile
        fields=('userprofile','image','aboutyou')

