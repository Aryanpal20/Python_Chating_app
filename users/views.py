from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer, GetUserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken  
from .models import User
from django.shortcuts import get_object_or_404

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
        user = User.objects.filter(first_name__icontains = request.query_params.get('name'))
        serializer = GetUserSerializer(user, many=True)
        return Response (serializer.data)

       