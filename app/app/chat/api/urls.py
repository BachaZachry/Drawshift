from django.urls import path, include, re_path
from .views import DrawingAPIView

urlpatterns = [
    path('drawing/', DrawingAPIView.as_view())
]
