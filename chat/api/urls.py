from django.urls import path, re_path
from .views import DiagramAPIView, DrawingAPIView, RetrieveSingleDrawingAPIView

urlpatterns = [
    path("drawing/", DrawingAPIView.as_view()),
    re_path(r"^drawing/(?P<pk>\d+)/", RetrieveSingleDrawingAPIView.as_view()),
    path("diagram/", DiagramAPIView.as_view()),
]
