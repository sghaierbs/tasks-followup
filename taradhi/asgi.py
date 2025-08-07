"""
ASGI config for taradhi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import notifications.routing

# Only set the environment variable if it's not already defined
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'taradhi.settings.prod'
    print("------------ASGI DEFAULT: PROD---------------------")
else:
    print(f"------------ASGI USING: {os.environ['DJANGO_SETTINGS_MODULE']} ---------------------")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(notifications.routing.websocket_urlpatterns)
    ),
})