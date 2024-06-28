from chat.api.serializers import DrawingSerializer, DiagramSerializer
from chat.models import Drawing, Diagram
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response


class DrawingAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = DrawingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        drawing = serializer.save()
        return Response(
            {
                "drawing": DrawingSerializer(
                    drawing, context=self.get_serializer_context()
                ).data,
            }
        )

    def get_queryset(self):
        return Drawing.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveSingleDrawingAPIView(generics.RetrieveAPIView):
    serializer_class = DrawingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Drawing.objects.all()


class DiagramAPIView(generics.GenericAPIView):
    serializer_class = DiagramSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Diagram.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        diagram = serializer.save()
        return Response(
            {
                "diagram": DiagramSerializer(
                    diagram, context=self.get_serializer_context()
                ).data,
            }
        )

    def get(self, request):
        serializer = self.get_serializer()
        user = serializer.context["request"].user
        print(Diagram.objects.filter(user=user))
        return Response(Diagram.objects.filter(user=user).values())
