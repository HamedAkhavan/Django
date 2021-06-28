from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status


from users.api.serializers import UserSerializer

class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny, ]


    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
