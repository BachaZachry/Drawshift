from django.urls import path, include, re_path
from .views import DiagramAPIView, DrawingAPIView

urlpatterns = [
    path('drawing/', DrawingAPIView.as_view()),
    path('diagram/', DiagramAPIView.as_view()),
]
