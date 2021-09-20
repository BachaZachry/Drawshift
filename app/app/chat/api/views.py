from app.app.chat.api.serializers import DiagramSerializer
from app.app.chat.models import Diagram
from chat.api.serializers import DrawingSerializer
from chat.models import Drawing
from rest_framework import generics, permissions
from rest_framework.response import Response


class DrawingAPIView(generics.GenericAPIView):
    serializer_class = DrawingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Drawing.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        drawing = serializer.save()
        return Response({
            "drawing": DrawingSerializer(drawing, context=self.get_serializer_context()).data,
        })

    def get(self, request):
        serializer = self.get_serializer()
        user = serializer.context['request'].user
        print(Drawing.objects.filter(user=user))
        return Response(Drawing.objects.filter(user=user).values())


class DiagramAPIView(generics.GenericAPIView):
    serializer_class = DiagramSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Diagram.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        diagram = serializer.save()
        return Response({
            "diagram": DiagramSerializer(diagram, context=self.get_serializer_context()).data,
        })

    def get(self, request):
        serializer = self.get_serializer()
        user = serializer.context['request'].user
        print(Diagram.objects.filter(user=user))
        return Response(Diagram.objects.filter(user=user).values())
