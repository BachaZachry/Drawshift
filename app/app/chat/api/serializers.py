from chat.models import Drawing
from rest_framework import serializers


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ['svg_file', 'title']
        extra_kwargs = {'user': {'default': serializers.CurrentUserDefault()}}
