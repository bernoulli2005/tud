from rest_framework import viewsets
from .models import Chat, Message
from django.db import transaction
from .serializers import ChatSerializer, MessageSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Message
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import exceptions
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.response import Response
from main_login.models import CustomUser 
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class InvalidToken(Exception):
    pass

class JWTCookieAuthentication(BaseAuthentication):

    cookie_name = 'access_token'

    @classmethod
    def get_cookie_name(cls):
        return cls.cookie_name

    def decode(self, token):
        """
        Decodes the given JWT token, verifying its signature and validity.
        """
        try:
            # Decode the token using PyJWT
            # This will use Django's SECRET_KEY and the JWT's algorithm (by default HS256)
            # to decode and verify the token.
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise InvalidToken("Token has expired")
        except jwt.DecodeError:
            raise InvalidToken("Token decode failed")
        except jwt.InvalidTokenError:
            raise InvalidToken("Token is invalid")

    def authenticate(self, request):
        raw_token = request.COOKIES.get(self.get_cookie_name())
        if raw_token is None:
            return None
        
        # Decoding and authenticating the token
        try:
            validated_token = self.decode(raw_token)
        except InvalidToken as e:
            raise AuthenticationFailed(str(e))
        
        # You should now extract the user information from the validated_token
        # and retrieve the user object, then return it along with the token for DRF's internal processing.
        # Assuming user_id is stored in the token:
        user_id = validated_token.get('user_id')
        if not user_id:
            raise AuthenticationFailed("No user found in the token.")

        try:
            # Replace this with your User model or however you handle user objects.
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found.")
        
        return (user, raw_token) 

@authentication_classes([JWTCookieAuthentication])
@permission_classes([IsAuthenticated])
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()  # Make a copy of the request data
        participants = data.get('participants', [])

        # Add the current user to participants if not already present
        if request.user.id not in participants:
            participants.append(request.user.id)
        data['participants'] = participants

        # Use a transaction to ensure atomicity
        with transaction.atomic():
            chat = Chat.objects.create()
            chat.participants.set(participants)
            chat.save()

        serializer = self.get_serializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    # Assuming you want the same authentication and permissions for messages:
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer