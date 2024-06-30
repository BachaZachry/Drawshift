from chat.api.serializers import DrawingSerializer, DiagramSerializer
from chat.models import Drawing, Diagram
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer


class DrawingAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = DrawingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Create a drawing",
        description="Allows creating a new drawing.",
        responses={
            201: inline_serializer(
                name="create-drawing",
                fields={
                    "drawing": DrawingSerializer(),
                },
            ),
        },
        examples=[
            OpenApiExample(
                "Example drawing creation",
                value={
                    "title": "My Drawing",
                    "path": "canvas_data",
                    "base64_image": "base64_image",
                },
                request_only=True,
            ),
        ],
    )
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

    @extend_schema(
        summary="list drawings",
        description="Allows listing all drawings for the authenticated user.",
        responses={200: DrawingSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@extend_schema(
    summary="Retrieve a single drawing",
    description="Retrieves details of a specific drawing by its ID.",
    responses={200: DrawingSerializer},
)
class RetrieveSingleDrawingAPIView(generics.RetrieveAPIView):
    serializer_class = DrawingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Drawing.objects.all()


class DiagramAPIView(generics.GenericAPIView):
    serializer_class = DiagramSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Diagram.objects.all()

    @extend_schema(
        summary="Create a diagram",
        description="Allows creating a new diagram.",
        responses={
            201: inline_serializer(
                name="create-diagram",
                fields={
                    "diagram": DiagramSerializer(),
                },
            ),
        },
        examples=[
            OpenApiExample(
                "Example diagram creation",
                value={
                    "title": "My Drawing",
                    "elements": "canvas_data",
                },
                request_only=True,
            ),
        ],
    )
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

    def get_queryset(self):
        return Diagram.objects.filter(user=self.request.user)

    @extend_schema(
        summary="list diagrams",
        description="Allows listing all diagrams for the authenticated user.",
        responses={200: DiagramSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@extend_schema(
    summary="Retrieve a single diagram",
    description="Retrieves details of a specific diagram by its ID.",
    responses={200: DiagramSerializer},
)
class RetrieveSingleDiagramAPIView(generics.RetrieveAPIView):
    serializer_class = DiagramSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Diagram.objects.all()
