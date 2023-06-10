from django.urls import path
from .views import RegisterAPI, LoginAPI, SearchUserView, UserChatConsumer
# from .consumers import ChatConsumer

urlpatterns = [ 
    path("register/",RegisterAPI.as_view(),name="register"),
    path("login/",LoginAPI.as_view(), name='Login'),
    path('get_user/', SearchUserView.as_view(), name='getuser'),
    path('api/chat/', UserChatConsumer.as_asgi()),
]
