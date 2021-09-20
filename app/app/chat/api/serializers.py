from app.app.chat.models import Diagram
from chat.models import Drawing
from rest_framework import serializers


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ['path', 'title', 'user']
        extra_kwargs = {'user': {'default': serializers.CurrentUserDefault()}}


class DiagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagram
        fields = ['elements', 'title', 'user']
        extra_kwargs = {'user': {'default': serializers.CurrentUserDefault()}}
