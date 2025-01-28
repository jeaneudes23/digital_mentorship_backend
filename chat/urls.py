from django.urls import path
from . import views

urlpatterns = [
  path('register', views.registerUser, name="register"),
  path('auth', views.getAuthUser , name='chats'),
  path('users',views.UserListView.as_view(), name="users"),
  path('users-stats', views.getUsersStats, name="users_stats"),
  path('chatrooms/user', views.ChatRoomListApiView.as_view(),name="user_chatrooms"),
  path('chatrooms/generate', views.getChatRoom , name="getChatRoom"),
  path('chatrooms/messages/<int:chatroom_id>', views.ChatRoomMessageListApiView.as_view(),name="chatroom_messages"),
  path('chatrooms/<int:chatroom_id>', views.ChatRoomDetailApiView.as_view(),name="chatroom"),
  path('messages/send', views.sendMessage , name='send_message')
]

