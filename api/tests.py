from django.contrib.auth.models import User
from api.views import UserViewSet
from rest_framework.test import APIRequestFactory, force_authenticate

factory = APIRequestFactory()
user = User.objects.get(username='admin')
view = UserViewSet.as_view()

request = factory.get('http://127.0.0.1:8000/api/users')
force_authenticate(request, user=user)
response = view(request)
