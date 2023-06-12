from django.urls import path
from .views import RegisterAPI, LoginAPI, SearchUserView, ChatRoomView, MessagesView


urlpatterns = [ 
    path("register/",RegisterAPI.as_view(),name="register"),
    path("login/",LoginAPI.as_view(), name='Login'),
    path('get_user/', SearchUserView.as_view(), name='getuser'),
    path('chats', ChatRoomView.as_view(), name='chatRoom'),
	path('chats/<str:roomId>/messages', MessagesView.as_view(), name='messageList'),
	path('users/<int:userId>/chats', ChatRoomView.as_view(), name='chatRoomList'),
]
