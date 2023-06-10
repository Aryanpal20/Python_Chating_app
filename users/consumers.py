from channels.generic.websocket import AsyncJsonWebsocketConsumer
from djangochannelsrestframework.decorators import action
from .models import UserChat


class ChatConsumer(AsyncJsonWebsocketConsumer):
    print("dvkjbdvkjvbjvbdvbdbvd")
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    @action()
    async def chat_message(self, content):
        # Handle incoming chat message
        print("smhmvdsvhdhvd")
        sender = self.scope['user']
        receiver_id = content['receiver_id']
        message = content['message']

        # Save the chat message to the database
        user_chat = UserChat.objects.create(sender=sender, receiver_id=receiver_id, content=message)
        user_chat.save()

        # Broadcast the chat message to the receiver's WebSocket channel
        await self.channel_layer.group_send(
            str(receiver_id),
            {
                'type': 'send_message',
                'message': message,
            }
        )

    async def send_message(self, event):
        print("dshbvhdvbdmv")
        # Send the chat message to the WebSocket channel
        await self.send(text_data=event['message'])
        
