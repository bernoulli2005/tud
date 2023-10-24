from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, MessageViewSet
from . import consumers

# Configura el enrutador para tus vistas de API REST
router = DefaultRouter()
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    # Rutas para la API REST
    path('api/', include(router.urls)),

    # Ruta para el WebSocket
    re_path(r'ws/chat/(?P<token>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
