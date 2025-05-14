import asyncio
import httpx
from channels.layers import get_channel_layer
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async
from tracker.models import TrackedCoin  # Ensure this is correct based on your app name

class Command(BaseCommand):
    help = 'Fetch crypto prices for all tracked coins and broadcast to WebSocket group'

    async def fetch_prices(self, coin_ids):
        ids = ",".join(coin_ids)
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()

    async def broadcast_prices(self):
        channel_layer = get_channel_layer()

        while True:
            # ✅ Get unique coin IDs being tracked by any user
            coin_ids = await sync_to_async(
                lambda: list(
                    TrackedCoin.objects.values_list('coin_name', flat=True).distinct()
                )
            )()
            print(coin_ids)
            if coin_ids:
                prices = await self.fetch_prices(coin_ids)
                print("✅ Sending prices:", prices)

                await channel_layer.group_send(
                    "crypto_prices",
                    {
                        "type": "send_prices",
                        "prices": prices
                    }
                )
            else:
                print("⚠️ No tracked coins found. Skipping this cycle.")

            await asyncio.sleep(10)

    def handle(self, *args, **kwargs):
        asyncio.run(self.broadcast_prices())
