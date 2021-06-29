from django.contrib import admin
from django.urls import path
from users.api.views import UserViewSet


urlpatterns = [
    path('register', UserViewSet.as_view({'post': 'create'}), name='register'),
]
