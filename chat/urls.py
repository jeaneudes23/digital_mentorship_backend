from django.urls import path
from . import views

urlpatterns = [
  path('register', views.registerUser, name="register"),
  path('auth', views.getAuthUser , name='chats'),
  path('users',views.UserListView.as_view(), name="users"),
  path('users-stats', views.getUsersStats, name="users_stats"),
]

