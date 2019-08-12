from django.urls import path, include
from rest_framework import routers

from api.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
