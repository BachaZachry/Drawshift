from itertools import chain
from chat.api.serializers import DrawingSerializer, DiagramSerializer, BoardsSerializer
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


class RetrieveUserBoardsAPIView(generics.GenericAPIView):
    serializer_class = BoardsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Get combined data from drawings and diagrams",
        description="Retrieves data from drawings and diagrams for the authenticated user.",
        responses={
            200: BoardsSerializer,
        },
        examples=[
            OpenApiExample(
                "Successful Response",
                value={
                    "drawings": [
                        {
                            "id": 1,
                            "title": "title1",
                            "path": ["x", "y"],
                            "base64_image": "string",
                        },
                        {
                            "id": 2,
                            "title": "title2",
                            "path": ["x", "y"],
                            "base64_image": "string",
                        },
                    ],
                    "diagrams": [
                        {
                            "id": 1,
                            "title": "title1",
                            "nodes": ["x", "y"],
                            "edges": ["x", "y"],
                            "base64_image": "string",
                        },
                        {
                            "id": 2,
                            "title": "title2",
                            "nodes": ["x", "y"],
                            "edges": ["x", "y"],
                            "base64_image": "string",
                        },
                    ],
                },
                response_only=True,
                status_codes=["200"],
            ),
        ],
    )
    def get(self):
        diagrams = Diagram.objects.filter(user=self.request.user)
        drawings = Drawing.objects.filter(user=self.request.user)
        boards_data = {"drawings": drawings, "diagrams": diagrams}

        serializer = BoardsSerializer(boards_data)
        return Response(serializer.data)
