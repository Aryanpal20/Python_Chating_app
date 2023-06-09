from django.urls import path
from .views import RegisterAPI, LoginAPI, SearchUserView


urlpatterns = [ 
    path("register/",RegisterAPI.as_view(),name="register"),
    path("login/",LoginAPI.as_view(), name='Login'),
    path('get_user/', SearchUserView.as_view(), name='getuser')
]