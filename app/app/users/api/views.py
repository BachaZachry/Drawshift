from rest_framework import generics,permissions,mixins
from .serializers import LoginSerializer,RegisterSerializer,UserSerializer,\
    KnoxSerializer,
from users.models import User
from rest_framework.response import Response
from knox.models import AuthToken
from allauth.account.adapter import get_adapter
from dj_rest_auth.views import LoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.serializers import SocialLoginSerializer


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

class KnoxLoginView(LoginView):
    serializer_class = KnoxSerializer

    def get_response(self):
        serializer_class = self.get_response_serializer()
        data = {
            'token': self.token,
            'user': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email
        }
        serializer = serializer_class(instance=data)

        return Response(serializer.data, status=200)


class SocialLoginView(KnoxLoginView):
    serializer_class = SocialLoginSerializer

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter