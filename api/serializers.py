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

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfileInfo
        fields = ['user', 'portfolio_site', 'profile_image']


class TestSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSession
        fields = ['no_of_questions', 'created_at', 'finished_at']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['user', 'question', 'session', 'choice']
