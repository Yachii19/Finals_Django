# user_management/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='profile.get_gender_display')
    birthday = serializers.DateField(source='profile.birthday')
    registration_date = serializers.DateTimeField(source='profile.registration_date')
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'gender', 'birthday', 'registration_date')