from django.contrib.auth.models import User

from rest_framework import viewsets, permissions, pagination
from rest_framework.response import Response

from .serializers import (UserSerializer, UserProfileSerializer,
                          TestSessionSerializer, AnswerSerializer)

from basicapp.models import (UserProfileInfo, TestSession,
                             Question, Answer)


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfileInfo.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class TestSessionViewSet(viewsets.ModelViewSet):
    serializer_class = TestSessionSerializer
    queryset = TestSession.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = [permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination
