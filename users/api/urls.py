from django.urls import path, include, re_path
from .views import CreateTeam, GithubLogin, InviteAPIView, RegisterAPI, LoginAPI, LoadUser,\
    GoogleLogin, RespondToAnInvitation
from knox.views import LogoutView

urlpatterns = [
    path('login/', LoginAPI.as_view()),
    path('loaduser/', LoadUser.as_view()),
    path('register/', RegisterAPI.as_view()),
    path('logout/', LogoutView.as_view()),
    re_path(r'^rest-auth/google/$', GoogleLogin.as_view(), name='google_login'),
    path('invite/', InviteAPIView.as_view()),
    re_path(r'^invite/(?P<pk>\d+)/$', RespondToAnInvitation.as_view()),
    path('createteam/', CreateTeam.as_view()),
    re_path(r'^rest-auth/github/$', GithubLogin.as_view(), name='github_login'),
]
