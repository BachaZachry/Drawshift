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
            await self.broadcast_canvas_update(canvas_data)

    async def broadcast_canvas_update(self, canvas_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "send_canvas_update", "canvas_data": canvas_data},
        )

    async def send_canvas_update(self, event):
        canvas_data = event["canvas_data"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "canvas_update",
                    "canvas_data": canvas_data,
                }
            )
        )
