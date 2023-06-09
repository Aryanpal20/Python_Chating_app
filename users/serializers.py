from rest_framework import serializers
from .models import User, UserChat


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'gender', 'mobile_no', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'id', 'first_name',)


class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChat
        fields = ['sender', 'receiver', 'content', 'timestamp']