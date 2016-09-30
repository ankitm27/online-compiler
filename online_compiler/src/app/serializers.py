from rest_framework import serializers
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True, style={'placeholder': 'Username'})
    password = serializers.CharField(max_length=100, required=True, style={'input_type': 'Password', 'placeholder': 'Password'})

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True, style={'placeholder': 'Username'})
    email = serializers.EmailField(max_length=100, required=True, style={'placeholder': 'Email'})
    password = serializers.CharField(max_length=100, required=True, style={'input_type': 'password', 'placeholder': 'Password', 'id':'password'})
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        username = validated_data['username']
        if User.objects.filter(username=username).count():
            error = "Username "+ username +" already exist."
            raise serializers.ValidationError(error)
            
        password = validated_data.pop('password', None)
        if password is not None:
            password = make_password(password, salt=None, hasher='default')
            validated_data.update({'password':password})
        else:
            validated_data.update({'password':''})
        return User.objects.create(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True, style={'placeholder': 'Username', 'read_only':True})
    email = serializers.EmailField(max_length=100, required=True, style={'placeholder': 'Email'})
    first_name = serializers.CharField(max_length=100, required=True, style={'placeholder': 'First name'})
    last_name = serializers.CharField(max_length=100, required=True, style={'placeholder': 'Last name'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=100, required=True, style={'input_type': 'Password', 'placeholder': 'Current Password'})
    new_password = serializers.CharField(max_length=100, required=True, style={'input_type': 'Password', 'placeholder': 'New Password'})
    confirm_password = serializers.CharField(max_length=100, required=True, style={'input_type': 'Password', 'placeholder': 'Confirm Password'})

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True, style={'placeholder': 'Name'})
    email = serializers.EmailField(max_length=100, required=True, style={'placeholder': 'Email'})

class ForgetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True, style={'placeholder': 'Username', 'read_only':True})