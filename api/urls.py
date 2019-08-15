from django.urls import path, include
from rest_framework import routers

from api.views import UserViewSet, UserProfileViewSet, TestSessionViewSet, AnswerViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='user'),
router.register(r'profile', UserProfileViewSet, base_name='profile')
router.register(r'test', TestSessionViewSet, base_name='test')
router.register(r'answer', AnswerViewSet, base_name='answer')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
