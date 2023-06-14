from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import UserSerializer, GetUserSerializer, ChatMessageSerializer, ChatRoomList
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken  
from .models import User, ChatRoom, ChatMessage
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status

# Create your views here.

class RegisterAPI(APIView):

    def post(self, request):

        # Extract data from the request
        data = request.data

        data['username'] = data['email']
        # Initialize a UserSerializer with the request data
        serializer = UserSerializer(data=data)

        # Validate the request data and save the new user if validation is successful
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return a success message in the response
        return Response({"message" : "User register successfully."}, status=200)

class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return Response({'error': "Invalid username"}, status=status.HTTP_401_UNAUTHORIZED)

        check_pwd = check_password(password, user.password)

        if check_pwd:
            refresh = RefreshToken.for_user(user)
            data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response({"message" : "Login successfully.", "data" : data}, status=200)

        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    

class SearchUserView(APIView):
    def get(self, request):
        name = request.query_params.get('name')
        user_id = request.query_params.get('id')
        queryset = User.objects.all()

        if name:
            queryset = queryset.filter(first_name__icontains=name)

        if user_id:
            queryset = queryset.filter(id=user_id)

        serializer = GetUserSerializer(queryset, many=True)
        return Response(serializer.data)

    
    
class ChatRoomView(APIView):
    def get(self, request, userId):
        room = ChatRoom.objects.filter(member_1=userId) | ChatRoom.objects.filter(member_2=userId)

        serializer = ChatRoomList(room, many=True)
        return Response(serializer.data)

class MessagesView(ListAPIView):
    serializer_class = ChatMessageSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        roomId = self.kwargs['roomId']
        return ChatMessage.objects.filter(room_ID=roomId).order_by('-timestamp')
       