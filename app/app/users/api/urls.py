from django.urls import path,include
from .views import RegisterAPI,LoginAPI,LoadUser

urlpatterns = [
    path('login/',LoginAPI.as_view()),
    path('loaduser/',LoadUser.as_view()),
    path('register/',RegisterAPI.as_view()),
]