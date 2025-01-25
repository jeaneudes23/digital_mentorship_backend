from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.contrib.auth.models import User
from .models import Profile
from .serializers import UserSerializer , ProfileSerializer
from django.db.models import Prefetch
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import BasePagination
from .pagination import CustomPagination
from django.db import models


# Create your views here.

@api_view(['GET',])
def ping(request):
  return JsonResponse({"message": "ping"})

@api_view(['GET',])
def getAuthUser(request):
  if (request.user.is_authenticated):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

  return Response({'authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST',])
def registerUser(request):
  serializer = UserSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    user = serializer.data
    profile_data = request.data.copy()
    profile_data["user"] = user['id']
    profileSerializer = ProfileSerializer(data=profile_data)
    if profileSerializer.is_valid():
      profileSerializer.save()
    
    return Response({
      "message": "User Created Successfully",
      "user": serializer.data,
    }, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


  
  
  
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET',])
def getUsersStats(request):
  students_count = User.objects.filter(profile__role='student').count()
  staffs_count = User.objects.filter(profile__role='staff').count()
  therapists_count = User.objects.filter(profile__role='therapist').count()
  
  stats = {"students_count":students_count,"staffs_count": staffs_count,"therapists_count": therapists_count}
  
  return Response(stats)

class UserListView(ListAPIView):
  serializer_class = UserSerializer
  pagination_class = CustomPagination
  
  def get_queryset(self):
    role = self.request.query_params.get('role')
    q = self.request.query_params.get('q')
    
    queryset = User.objects.filter(is_staff=False)
    
    if role in ['staff','student','therapist']:
      queryset = queryset.filter(profile__role=role)
    if q:
      queryset = queryset.filter(models.Q(first_name__icontains=q) | models.Q(last_name__icontains=q))
    
    return queryset