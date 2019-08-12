from django.contrib.auth.models import User

from rest_framework import viewsets
from .serializers import (UserSerializer, TestSessionSerializer,
                          QuestionSerializer, AnswerSerializer)

from basicapp.models import (UserProfileInfo, TestSession,
                             Question, Answer)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

