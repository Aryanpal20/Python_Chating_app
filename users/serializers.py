from rest_framework import serializers
from .models import User, ChatRoom, ChatMessage


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'gender', 'mobile_no', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # chatRoom = ChatRoom.objects.create(
		# 	type="SELF", name=user.first_name +" "+ user.last_name
		# )
        # chatRoom.member.add(user.id)
	
        return user

    

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'id', 'first_name',)


class ChatRoomSerializer(serializers.ModelSerializer):
	member = UserSerializer(many=True, read_only=True)
	members = serializers.ListField(write_only=True)

	def create(self, validatedData):
		memberObject = validatedData.pop('members')
		chatRoom = ChatRoom.objects.create(**validatedData)
		chatRoom.member.set(memberObject)
		return chatRoom

	class Meta:
		model = ChatRoom
		exclude = ['id']

class ChatMessageSerializer(serializers.ModelSerializer):
	userName = serializers.SerializerMethodField()

	class Meta:
		model = ChatMessage
		exclude = ['id', 'sender']

	def get_userName(self, Obj):
		return Obj.reciever.first_name + ' ' + Obj.reciever.last_name
	