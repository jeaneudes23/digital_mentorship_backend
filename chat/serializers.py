from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['id','user','role','image','department','level_of_education','document']
  
class UserSerializer(serializers.ModelSerializer):
  profile = ProfileSerializer(required=False)
  class Meta:
    model = User
    fields = ['id','username', 'email','first_name','last_name','password','profile']
    extra_kwargs = {
        'password': {'write_only': True}  
    }
    
  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    return user 