from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.contrib.auth.models import User
from .models import Profile , ChatRoom , ChatRoomUser, Message
from .serializers import UserSerializer , ProfileSerializer, ChatRoomSerializer , MessageSerializer
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
  
  
@api_view(['GET',]) 
def getChatRoom(request):
  user_from = request.user
  user_to = User.objects.get(id=request.query_params.get('user_to'))
  
  chat_room = ChatRoom.objects.filter(
    is_private=True,
    users=user_from
  ).filter(
    users=user_to
  ).distinct().first()
  
  if not chat_room:
    chat_room = ChatRoom.objects.create(is_private=True,admin=user_from)
    ChatRoomUser.objects.create(user=user_from,chatRoom=chat_room)
    ChatRoomUser.objects.create(user=user_to,chatRoom=chat_room)
  
  serializer = ChatRoomSerializer(chat_room)
  return Response(serializer.data)


class ChatRoomDetailApiView(RetrieveAPIView):
  queryset = ChatRoom.objects.all()
  serializer_class = ChatRoomSerializer

  def get_object(self):
    try:
      chat_room = ChatRoom.objects.get(id=self.kwargs['chatroom_id'])
      if (chat_room.is_private and self.request.user not in chat_room.users.all()):
          raise PermissionDenied("You are not part of this chat room.")
      return chat_room
    except ChatRoom.DoesNotExist:
      raise NotFound("Chat room not found.")
  
  
class ChatRoomListApiView(ListAPIView):
  serializer_class = ChatRoomSerializer
  permission_classes = [IsAuthenticated]
  
  def get_queryset(self):
    queryset = ChatRoom.objects.filter(users = self.request.user).order_by('-updated_at')
  
    q = self.request.query_params.get('q')
    
    if (q):
      queryset = queryset.filter(users__first_name__icontains=q) | queryset.filter(users__last_name__icontains=q)
    
    return queryset
  
class ChatRoomMessageListApiView(ListAPIView):
  serializer_class = MessageSerializer
  permission_classes = [IsAuthenticated]
  
  def get_queryset(self):
    queryset = Message.objects.filter(chatRoom__id=self.kwargs['chatroom_id'])
    return queryset
  
@api_view(['POST',])
def sendMessage(request):
  content = request.data.get('content')
  chatroom_id = request.data.get('chatroom_id')
  sender = request.user
  
  try: 
    chatRoom = ChatRoom.objects.get(id=chatroom_id)
    if (chatRoom.is_private and sender not in chatRoom.users.all()):
      raise PermissionDenied("You are not part of this chat room.")
    message = Message.objects.create(
        content=content,
        chatRoom=chatRoom,
        sender=sender
    )
    chatRoom.lastMessage = message
    chatRoom.updated_at = message.sent_at
    chatRoom.save()
    serializer = MessageSerializer(message)
    return Response(serializer.data)
  except:
    raise NotFound('Not found ndn')
