from django.urls import path,include,re_path
from .views import RegisterAPI,LoginAPI,LoadUser,GoogleLogin

urlpatterns = [
    path('login/',LoginAPI.as_view()),
    path('loaduser/',LoadUser.as_view()),
    path('register/',RegisterAPI.as_view()),
    re_path(r'^rest-auth/google/$', GoogleLogin.as_view(), name='google_login'),
]