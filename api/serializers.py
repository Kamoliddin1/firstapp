from rest_framework import serializers
from django.contrib.auth.models import User
from basicapp.models import (UserProfileInfo,
                             TestSession,
                             Question,
                             Answer)


class UserSerializer(serializers.ModelSerializer):
    portfolio_site = serializers.PrimaryKeyRelatedField(queryset=UserProfileInfo.objects.all(),
                                                        source='user_profile.portfolio_site',
                                                        required=False, default=None)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'portfolio_site']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TestSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSession


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
