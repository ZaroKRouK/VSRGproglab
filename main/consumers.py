import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'votes',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'votes',
            self.channel_name
        )

    async def vote_update(self, event):
        message = event.get('message', {})
        
        user_vote = message.get('user_vote')
        if user_vote is None:
            # Логируем предупреждение, что ключ отсутствует
            print("Warning: 'user_vote' key missing in message")
            # Можно либо отправить пустой user_vote, либо пропустить его
            user_vote = None
        
        await self.send(text_data=json.dumps({
            'type': 'vote_update',
            'map_id': message.get('map_id'),
            'likes': message.get('likes'),
            'dislikes': message.get('dislikes'),
            'user_vote': user_vote
        }))