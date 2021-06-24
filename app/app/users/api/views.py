from rest_framework import generics, permissions, mixins
from .serializers import InviteSerializer, LoginSerializer, RegisterSerializer, TeamSerializer, \
    KnoxSerializer, UserSerializer
from users.models import User, Invite
from rest_framework.response import Response
from knox.models import AuthToken
from allauth.account.adapter import get_adapter
from dj_rest_auth.views import LoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from users.permissions import canInvite, canCreateTeam


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


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter


class CreateTeam(generics.GenericAPIView):
    serializer_class = TeamSerializer
    permission_classes = [canCreateTeam]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = serializer.save()
        user = self.request.user
        user.team = team
        user.is_leader, user.can_invite = True, True
        user.save()

        return Response({
            "Team": team.id,
            "user": user.id
        })


class InviteAPIView(generics.GenericAPIView):
    serializer_class = InviteSerializer
    permission_classes = [canInvite]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Creating the invite
        invite = serializer.save()
        return Response({
            'Invite': InviteSerializer(invite, context=self.get_serializer_context()).data,
            'Invite Id': invite.pk,
        })


class RespondToAnInvitation(generics.RetrieveUpdateAPIView):
    serializer_class = InviteSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Invite.objects.all()

    def get_queryset(self):
        serializer = self.get_serializer()
        receiver = serializer.context['request'].user
        # Return only the invitations sent to that specific user
        return Invite.objects.filter(receiver=receiver)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['status'] == 'A':
            receiver = serializer.context['request'].user
            sender_id = serializer.validated_data['sender']
            sender = User.objects.get(pk=sender_id)
            receiver.team = sender.team
            receiver.save()
        return self.update(request, *args, **kwargs)
