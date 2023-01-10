# chat/consumers.py
import json
import random

import redis
from channels.generic.websocket import AsyncWebsocketConsumer

from GameWS import settings

redis_instance = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.pin = self.scope["url_route"]["kwargs"]["pin"]
        self.room_group_name = "chat_%s" % self.pin
        self.user_id = random.randrange(100000, 999999)

        redis_instance.set(f"game:{self.pin}:player:{self.user_id}", "True")

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "player_connect", "user_id": self.user_id}
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg_type = text_data_json["type"]

        if msg_type == "key_event":
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "key_event",
                    "user_id": self.user_id,
                    "event": text_data_json["event"],
                    "key": text_data_json["key"],
                    "x": text_data_json["x"],
                    "y": text_data_json["y"],
                }
            )
        elif msg_type == "position":
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "position",
                    "user_id": self.user_id,
                    "x": text_data_json["x"],
                    "y": text_data_json["y"],
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        print(message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    # Receive message from room group
    async def key_event(self, event):
        # Send message to WebSocket
        if self.user_id != event["user_id"]:
            await self.send(text_data=json.dumps(
                {
                    "type": "key_event",
                    "user_id": event["user_id"],
                    "event": event["event"],
                    "key": event["key"],
                    "x": event["x"],
                    "y": event["y"],
                }
            ))

    # Receive message from room group
    async def position(self, event):
        # Send message to WebSocket
        if self.user_id != event["user_id"]:
            await self.send(text_data=json.dumps(
                {
                    "type": "position",
                    "user_id": event["user_id"],
                    "x": event["x"],
                    "y": event["y"],
                }
            ))

    # Receive message from room group
    async def player_connect(self, event):
        # Send message to WebSocket
        if self.user_id != event["user_id"]:
            await self.send(text_data=json.dumps({"type": "player_connect", "user_id": self.user_id}))
