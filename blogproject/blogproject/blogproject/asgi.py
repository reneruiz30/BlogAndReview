import os
from django.core.asgi import get_asgi_application # Import this first
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Set the Django settings module BEFORE any Django app code is imported
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogproject.settings')

# Initialize Django's ASGI application. This loads the Django app registry.
# This must happen before importing any Django-dependent modules from your apps.
django_asgi_app = get_asgi_application()

# Now it's safe to import your app's routing
import blogapp.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app, # Use the initialized Django ASGI app for HTTP
    "websocket": AuthMiddlewareStack(
        URLRouter(
            blogapp.routing.websocket_urlpatterns
        )
    ),
})