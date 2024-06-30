import json
from channels.generic.websocket import AsyncWebsocketConsumer

# from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.user = self.scope['user']
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Permission here
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Send message to room group

        if data.get("type") == "canvas_update":
            canvas_data = data.get("canvas_data")
            user = data.get("user_id")
            await self.broadcast_canvas_update(canvas_data, user)

        if data.get("type") == "diagram_update":
            diagram_data = data.get("diagram_data")
            operation = data.get("operation")
            user = data.get("user_id")
            await self.broadcast_diagram_update(diagram_data, operation, user)

    async def broadcast_canvas_update(self, canvas_data, user):
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "send_canvas_update", "canvas_data": canvas_data, "user_id": user},
        )

    async def broadcast_diagram_update(self, diagram_data, operation, user):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_diagram_update",
                "diagram_data": diagram_data,
                "operation": operation,
                "user_id": user,
            },
        )

    async def send_canvas_update(self, event):
        canvas_data = event["canvas_data"]
        user = event["user_id"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "canvas_update",
                    "canvas_data": canvas_data,
                    "user_id": user,
                }
            )
        )

    async def send_diagram_update(self, event):
        diagram_data = event["diagram_data"]
        operation = event["operation"]
        user = event["user_id"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "diagram_update",
                    "diagram_data": diagram_data,
                    "operation": operation,
                    "user_id": user,
                }
            )
        )
