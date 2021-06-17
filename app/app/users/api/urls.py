from django.urls import path, include, re_path
from .views import CreateTeam, InviteAPIView, RegisterAPI, LoginAPI, LoadUser,\
    GoogleLogin, RespondToAnInvitation

urlpatterns = [
    path('login/', LoginAPI.as_view()),
    path('loaduser/', LoadUser.as_view()),
    path('register/', RegisterAPI.as_view()),
    re_path(r'^rest-auth/google/$', GoogleLogin.as_view(), name='google_login'),
    path('invite/', InviteAPIView.as_view()),
    re_path(r'^invite/(?P<pk>\d+)/$', RespondToAnInvitation.as_view()),
    path('createteam/', CreateTeam.as_view()),
]
