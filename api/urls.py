from django.urls import path, include
from rest_framework import routers

from api.views import UserViewSet, UserProfileViewSet, TestSessionViewSet, AnswerViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='users'),
router.register(r'profile', UserProfileViewSet, base_name='profile')
router.register(r'test', TestSessionViewSet, base_name='test_sessions')
router.register(r'answer', AnswerViewSet, base_name='answer')

urlpatterns = [
    path('', include(router.urls)),

    path('rest-auth/', include('rest_auth.urls'))
]
