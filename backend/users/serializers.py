from rest_framework import serializers
from .models import User, ChatRoom, ChatMessage


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'gender',
            'mobile_no', 'first_name', 'last_name'
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class ChatMessageSerializer(serializers.ModelSerializer):
    userName = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        exclude = ['id', 'sender']

    def get_userName(self, Obj):
        return Obj.receiver.first_name + ' ' + Obj.receiver.last_name


class ChatRoomList(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = (
            'type', 'timestamp',
            'first_name', 'last_name', 'id'
        )

    def get_first_name(self, obj):
        user_id = self.context.get('user_id')
        if obj.member_1_id == user_id:
            return UserSerializer(obj.member_2).data['first_name']
        else:
            return UserSerializer(obj.member_1).data['first_name']

    def get_last_name(self, obj):
        user_id = self.context.get('user_id')
        if obj.member_1_id == user_id:
            return UserSerializer(obj.member_2).data['last_name']
        else:
            return UserSerializer(obj.member_1).data['last_name']

    def get_id(self, obj):
        user_id = self.context.get('user_id')
        if obj.member_1_id == user_id:
            return UserSerializer(obj.member_2).data['id']
        else:
            return UserSerializer(obj.member_1).data['id']
