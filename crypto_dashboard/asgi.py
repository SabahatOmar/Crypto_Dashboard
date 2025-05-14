import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import tracker.routing  # <-- we'll create this soon

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_dashboard.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            tracker.routing.websocket_urlpatterns
        )
    ),
})
