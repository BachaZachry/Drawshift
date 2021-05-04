from rest_framework import generics,permissions
from .serializers import LoginSerializer,RegisterSerializer,UserSerializer
from users.models import User
from rest_framework.response import Response
from knox.models import AuthToken


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # get data from request
        serializer = self.get_serializer(data=request.data)
        # Check if data is valid
        serializer.is_valid(raise_exception=True)
        # save user
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # Sending a token for an immediate login
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    # Allow anyone to access this view
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = AuthToken.objects.create(user)
        return Response({
            'token': token[1],
            'username': user.username,
        })


class LoadUser(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user