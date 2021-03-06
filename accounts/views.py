from rest_framework.response import Response
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from .serializers import UserSerializer

class RegisterUsers(generics.CreateAPIView):
    """RegisterUsers class is used for register url. Non-admin users are registered
    in this view.
    METHOD: POST
	BODY TO SEND:
		{
			“username”: “user”,
			“password”: “password”
		}
    URL : https://dry-gorge-19755.herokuapp.com/api/auth/register/
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        try:
            user = User.objects.get(username=username)
            return Response(
            data = {
                "message": "User with username " + username + " already exists."
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        except:
            if not username or not password:
                return Response(
                data = {
                    "message": "Username and password required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            new_user = User.objects.create_user(
                username=username, password=password
            )
            return Response(
            data = {
                "message": "User " + username + " is created"
            },
            status=status.HTTP_201_CREATED
            )

class RegisterAdminUsers(generics.CreateAPIView):
    """RegisterUsers class is used for register url. Admin users are registered
    in this view.
    METHOD: POST
	BODY TO SEND:
		{
			“username”: “user”,
			“password”: “password”
		}
    URL : https://dry-gorge-19755.herokuapp.com/api/auth/register/admin/
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        try:
            user = User.objects.get(username=username)
            return Response(
            data = {
                "message": "User with username " + username + " already exists."
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        except:
            if not username or not password:
                return Response(
                data = {
                    "message": "Username and password required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            new_user = User.objects.create_user(
                username=username, password=password, is_staff=True
            )
            return Response(
            data = {
                "message": "User " + username + " is created"
            },
            status=status.HTTP_201_CREATED
            )
