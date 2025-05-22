from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from users.serializers import UserProfileSerializer
from django.db import models
from datetime import datetime

# Add a UserProfile model that extends the User model
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

# Update the RegisterSerializer to include new fields
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    gender = serializers.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=False)
    birthday = serializers.DateField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'gender', 'birthday')
    
    def create(self, validated_data):
        # Extract profile-related data
        gender = validated_data.pop('gender', None)
        birthday = validated_data.pop('birthday', None)
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            gender=gender,
            birthday=birthday
        )
        
        return user

# Update the ProfileView to include the new fields
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        profile = user.profile  # Access the related profile
        
        return Response({
            'username': user.username,
            'email': user.email,
            'gender': profile.get_gender_display() if profile.gender else None,
            'birthday': profile.birthday,
            'registration_date': profile.registration_date
        })

# Update the UserProfileSerializer to include new fields
class UserProfileSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='profile.get_gender_display')
    birthday = serializers.DateField(source='profile.birthday')
    registration_date = serializers.DateTimeField(source='profile.registration_date')
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'gender', 'birthday', 'registration_date')

# The RegisterView and LoginView can remain the same as in your original code
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        # Flatten errors into a single string for Flutter
        error_messages = []
        for field, errors in serializer.errors.items():
            error_messages.extend(errors)
        return Response({'error': ' '.join(error_messages)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)