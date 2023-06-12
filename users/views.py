from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import UserSerializer, GetUserSerializer, ChatMessageSerializer, ChatRoomSerializer
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken  
from .models import User, ChatRoom, ChatMessage
from django.shortcuts import get_object_or_404
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

    def post(self, request, format=None):
        # Deserialize the request data using the AuthTokenSerializer
        serializer = AuthTokenSerializer(data=request.data)
        # Validate the deserialized data and raise an exception if validation fails
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=request.data["username"])

        # Get the user object from the validated data
        user = serializer.validated_data['user']
        # Generate a refresh token for the user
        refresh = RefreshToken.for_user(user)
        data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        # Return the response with the data and a 200 status code
        return Response({"message" : "Login successfully.", "data" : data}, status=200)
    

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
		chatRooms = ChatRoom.objects.filter(member=userId)
		serializer = ChatRoomSerializer(
			chatRooms, many=True, context={"request": request}
		)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		serializer = ChatRoomSerializer(
			data=request.data, context={"request": request}
		)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessagesView(ListAPIView):
	serializer_class = ChatMessageSerializer
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		roomId = self.kwargs['roomId']
		return ChatMessage.objects.\
			filter(chat__roomId=roomId).order_by('-timestamp')
       