from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from basicapp import views


urlpatterns = [
    path('test/', views.test_session, name='test'),
    path('result/', views.submit_test_session, name='submit_test_session'),
    
    path('register/', views.register, name='register'),
    path('login/',  auth_views.LoginView.as_view(template_name='basicapp/login.html'), name="login"),
    path('logout/',  auth_views.LogoutView.as_view(template_name='basicapp/logout.html'), name="logout"),
    path('profile/', views.profile, name='profile')

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)