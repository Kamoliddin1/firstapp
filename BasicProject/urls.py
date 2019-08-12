from django.contrib import admin
from django.urls import path, include
from basicapp import views


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index, name='index'),
    path('', include('basicapp.urls')),
    path('api/', include('api.urls')),

]
