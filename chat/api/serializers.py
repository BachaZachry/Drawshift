from chat.models import Drawing, Diagram
from rest_framework import serializers


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ["id", "path", "title", "user", "base64_image"]
        extra_kwargs = {"user": {"default": serializers.CurrentUserDefault()}}


class DiagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagram
        fields = ["id", "nodes", "edges", "title", "user", "base64_image"]
        extra_kwargs = {"user": {"default": serializers.CurrentUserDefault()}}


class BoardsSerializer(serializers.Serializer):
    diagrams = DiagramSerializer(many=True, read_only=True)
    drawings = DrawingSerializer(many=True, read_only=True)
