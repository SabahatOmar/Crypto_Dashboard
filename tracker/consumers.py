from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CryptoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("crypto_prices", self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({'message': 'Connected & joined crypto_prices group'}))

    async def disconnect(self, close_code):
        # Remove this client from the group
        await self.channel_layer.group_discard("crypto_prices", self.channel_name)

    async def send_prices(self, event):
        prices = event['prices']
        print("Sending prices:", json.dumps(prices, indent=2))

        await self.send(text_data=json.dumps(prices))