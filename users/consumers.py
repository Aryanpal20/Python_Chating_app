import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import User, ChatMessage, ChatRoom
import uuid

class ChatConsumer(AsyncWebsocketConsumer):
	def getUser(self, userId):
		return User.objects.get(id=userId)

	# def getOnlineUsers(self):
	# 	onlineUsers = OnlineUser.objects.all()
	# 	return [onlineUser.user.id for onlineUser in onlineUsers]

	# def addOnlineUser(self, user):
	# 	try:
	# 		OnlineUser.objects.create(user=user)
	# 	except:
	# 		pass

	# def deleteOnlineUser(self, user):
	# 	try:
	# 		OnlineUser.objects.get(user=user).delete()
	# 	except:
	# 		pass

	def saveMessage(self, message, userId, roomId):
		userObj = User.objects.get(id=userId)
		chatObj = ChatRoom.objects.get(roomId=roomId)
		chatMessageObj = ChatMessage.objects.create(
			sender=chatObj, reciever=userObj, message=message
		)
		return {
			'action': 'message',
			'user': userId,
			'roomId': roomId,
			'message': message,
			'userName': userObj.first_name + " " + userObj.last_name,
			'timestamp': str(chatMessageObj.timestamp)
		}

	# async def sendOnlineUserList(self):
	# 	onlineUserList = await database_sync_to_async(self.getOnlineUsers)()
	# 	chatMessage = {
	# 		'type': 'chat_message',
	# 		'message': {
	# 			'action': 'onlineUser',
	# 			'userList': onlineUserList
	# 		}
	# 	}
	# 	await self.channel_layer.group_send('onlineUser', chatMessage)

	# async def connect(self):
	# 	self.userId = self.scope['url_route']['kwargs']['userId']
	# 	print(self.userId, "xkdjvndvkj")
	# 	self.userRooms = await database_sync_to_async(
	# 		list
	# 	)(ChatRoom.objects.filter(member=self.userId))
	# 	for room in self.userRooms:
	# 		await self.channel_layer.group_add(
	# 			room.roomId,
	# 			self.channel_name
	# 		)
	# 	# await self.channel_layer.group_add('onlineUser', self.channel_name)
	# 	self.user = await database_sync_to_async(self.getUser)(self.userId)
	# 	# await database_sync_to_async(self.addOnlineUser)(self.user)
	# 	# await self.sendOnlineUserList()
	# 	await self.accept()

	async def test_connect(self, payload):
		json_body = json.loads(payload)
		sender = json_body['sender']
		reciever = json_body['reciever']
		self.room_name = uuid.v4()

		_, chat_room = ChatRoom.objects.get_or_create(member_1=sender, member_2 = reciever, roomId=self.room_name)


	async def connect(self):
		# self.room_name = self.scope["url_route"]["kwargs"]
		# if not self.room_name:
		# text_data_json = json.loads(text_data)
		# sender = text_data_json['sender']
		# reciever = text_data_json['reciever']
		# self.room_name = uuid.v4()
		# print(self.room_name)
		
		# self.room_group_name = "chat_%s" % self.room_name
		# print(self.room_group_name)

		# _, chat_room = ChatRoom.objects.get_or_create(roomId=self.room_group_name)

		# Join room group
		# await self.channel_layer.group_add(chat_room, self.channel_name)

		await self.accept()

		
	async def disconnect(self, close_code):
		print("dn dnmv")
		# await database_sync_to_async(self.deleteOnlineUser)(self.user)
		# await self.sendOnlineUserList()
		# for room in self.userRooms:
		# 	await self.channel_layer.group_discard(
		# 		room.roomId,
		# 		self.channel_name
		# 	)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		action = text_data_json['action']
		print("xjhvxhjvvcv")
		roomId = None
		print("skvbdsjvdjcv")
		chatMessage = {}
		if action == 'message':
			message = text_data_json['message']
			print(message, "xkjnxkjnvv")
			userId = text_data_json['user']
			print(userId, "djhbvhjvb")
			self.userRooms = await database_sync_to_async(
			list
			)(ChatRoom.objects.filter(member=self.userId))
			print(self.userRooms, "sckjb")
			roomId = self.userRooms[0].roomId
			print(roomId,"skjcbshcbs")
			chatMessage = await database_sync_to_async(
				self.saveMessage
			)(message, userId, roomId)
		elif action == 'typing':
			chatMessage = text_data_json
		await self.channel_layer.group_send(
			roomId,
			{
				'type': 'chat_message',
				'message': chatMessage
			}
		)

	async def chat_message(self, event):
		message = event['message']
		await self.send(text_data=json.dumps(message))
