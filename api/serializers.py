from rest_framework import serializers
from django.contrib.auth.models import User
from basicapp.models import (UserProfileInfo,
                             TestSession,
                             Question,
                             Answer)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfileInfo
        fields = ['id', 'user', 'portfolio_site', 'profile_image']


class TestSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSession
        fields = ['no_of_questions', 'created_at', 'finished_at']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['user', 'question', 'session', 'choice']
