from chat.api.serializers import DrawingSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response


class DrawingAPIView(generics.GenericAPIView):
    serializer_class = DrawingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        drawing = serializer.save()
        return Response({
            "drawing": DrawingSerializer(drawing, context=self.get_serializer_context()).data,
        })
