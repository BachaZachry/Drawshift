import json
from rest_framework import generics, permissions, status, serializers
from .serializers import (
    InviteSerializer,
    LoginSerializer,
    RegisterSerializer,
    TeamSerializer,
    KnoxSerializer,
    UserSerializer,
)
from users.models import User, Invite
from rest_framework.response import Response
from knox.models import AuthToken
from allauth.account.adapter import get_adapter
from dj_rest_auth.views import LoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from users.permissions import canInvite, canCreateTeam
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    inline_serializer,
)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Register a new user",
        description="Creates a new user account and returns the user data along with an authentication token.",
        request=RegisterSerializer,
        responses={
            201: inline_serializer(
                name="auth-response",
                fields={"user": UserSerializer(), "token": serializers.CharField()},
            )
        },
        examples=[
            OpenApiExample(
                "Example register request",
                value={
                    "username": "newuser",
                    "password": "securepassword123",
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        # get data from request
        serializer = self.get_serializer(data=request.data)
        # Check if data is valid
        serializer.is_valid(raise_exception=True)
        # save user
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                # Sending a token for an immediate login
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    # Allow anyone to access this view
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="User login",
        description="Authenticates a user and returns user data along with an authentication token.",
        request=LoginSerializer,
        responses={
            201: inline_serializer(
                name="auth-response",
                fields={"user": UserSerializer(), "token": serializers.CharField()},
            )
        },
        examples=[
            OpenApiExample(
                "Example login request",
                value={
                    "username": "existinguser",
                    "password": "securepassword123",
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


@extend_schema(
    summary="Load authenticated user data",
    description="Retrieves the data of the currently authenticated user.",
    responses={200: UserSerializer},
)
class LoadUser(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class SocialLoginView(LoginView):
    serializer_class = SocialLoginSerializer

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)

    def get_response(self):
        return Response(
            {
                "user": UserSerializer(
                    self.user, context=self.get_serializer_context()
                ).data,
                "token": self.token,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    summary="Google OAuth login",
    description="Authenticates a user using Google OAuth and returns user data along with an authentication token.",
    request=SocialLoginSerializer,
    responses={
        201: inline_serializer(
            name="auth-response",
            fields={"user": UserSerializer(), "token": serializers.CharField()},
        )
    },
    examples=[
        OpenApiExample(
            "Example google auth request",
            value={
                "access_token": "google_access_token",
            },
            request_only=True,
        ),
    ],
)
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


@extend_schema(
    summary="GitHub OAuth login",
    description="Authenticates a user using GitHub OAuth and returns user data along with an authentication token.",
    request=SocialLoginSerializer,
    responses={
        201: inline_serializer(
            name="auth-response",
            fields={"user": UserSerializer(), "token": serializers.CharField()},
        )
    },
    examples=[
        OpenApiExample(
            "Example github auth request",
            value={
                "access_token": "github_access_token",
            },
            request_only=True,
        ),
    ],
)
class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter


# Rest of the API endpoints are going to be revamped in the next feature release.
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

        return Response({"Team": team.id, "user": user.id})


class InviteAPIView(generics.GenericAPIView):
    serializer_class = InviteSerializer
    permission_classes = [canInvite]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Creating the invite
        invite = serializer.save()
        return Response(
            {
                "Invite": InviteSerializer(
                    invite, context=self.get_serializer_context()
                ).data,
                "Invite Id": invite.pk,
            }
        )


class RespondToAnInvitation(generics.RetrieveUpdateAPIView):
    serializer_class = InviteSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Invite.objects.all()

    def get_queryset(self):
        serializer = self.get_serializer()
        receiver = serializer.context["request"].user
        # Return only the invitations sent to that specific user
        return Invite.objects.filter(receiver=receiver)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["status"] == "A":
            receiver = serializer.context["request"].user
            sender_id = serializer.validated_data["sender"]
            sender = User.objects.get(pk=sender_id)
            receiver.team = sender.team
            receiver.save()
        return self.update(request, *args, **kwargs)
