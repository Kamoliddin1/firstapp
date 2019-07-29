from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from basicapp.models import TestSession
from basicapp.views import TestSessionArchiveView, ProfileView, ProfileUpdateView

from basicapp import views


urlpatterns = [
    path('test/', views.test_session, name='test'),
    path('test/<pk>', views.test_session, name='test'),
    path('result/', views.submit_test_session, name='submit_test_session'),

    path('register/', views.register, name='register'),
    path('login/',  auth_views.LoginView.as_view(template_name='basicapp/login.html'), name="login"),
    path('logout/',  auth_views.LogoutView.as_view(template_name='basicapp/logout.html'), name="logout"),
    path('profile/', login_required(ProfileView.as_view(date_field="created_at", allow_empty=True)), name='profile'),
    path('profile_archive/', TestSessionArchiveView.as_view(model=TestSession, date_field="created_at"),
         name='snippet_archive'),
    path('profile_edit/', login_required(ProfileUpdateView.as_view()), name='profile_edit'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


