from django.urls import path
from .views import (
    RegisterAPI, LoginAPI, SearchUserView,
    ChatRoomView, MessagesView, GetRoom, LogoutAPI
)


urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="register"),
    path("login/", LoginAPI.as_view(), name='Login'),
    path("logout/", LogoutAPI.as_view(), name="logout"),
    path('get_user/', SearchUserView.as_view(), name='getuser'),
    path(
        'chats/<str:roomId>/messages',
        MessagesView.as_view(),
        name='messageList'
    ),
    path(
        'users/<int:userId>/chats',
        ChatRoomView.as_view(),
        name='chatRoomList'
    ),
    path('get_room_Id/', GetRoom.as_view(), name='get_roomID'),
]
