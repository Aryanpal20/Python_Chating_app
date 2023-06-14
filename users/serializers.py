from rest_framework import serializers
from .models import User, ChatRoom, ChatMessage


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
        fields = ( 'id', 'first_name', 'last_name', 'email')
        


class ChatMessageSerializer(serializers.ModelSerializer):
	userName = serializers.SerializerMethodField()

	class Meta:
		model = ChatMessage
		exclude = ['id', 'sender']

	def get_userName(self, Obj):
		return Obj.receiver.first_name + ' ' + Obj.receiver.last_name
	

class ChatRoomList(serializers.ModelSerializer):

    class Meta:
        model = ChatRoom
        fields = ('__all__')
