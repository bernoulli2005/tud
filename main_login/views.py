from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from rest_framework import views, generics, response, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer
from django.core.mail import send_mail
from rest_framework import views, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import TempUser
from .serializers import TempUserSerializer, VerifyCodeSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import TempUser

User = get_user_model()

class RegisterView(views.APIView):
    serializer_class = TempUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            temp_user = serializer.save()
            temp_user.generate_verification_code()
            send_mail(
                'Tu código de verificación',
                f'Tu código de verificación es {temp_user.verification_code}',
                'from@example.com',
                [temp_user.email]
            )
            return Response({'message': 'Código enviado'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyCodeView(views.APIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            code = serializer.validated_data.get('code')
            try:
                temp_user = TempUser.objects.get(email=email, verification_code=code)
                User.objects.create_user(
                    email=temp_user.email,
                    password=temp_user.password
                )
                temp_user.delete()  # Eliminar el registro temporal
                return Response({'message': 'Registro exitoso'}, status=status.HTTP_201_CREATED)
            except TempUser.DoesNotExist:
                return Response({'error': 'Código incorrecto o usuario no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            
            if user:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                response = Response({'access_token': access_token})
                response.set_cookie(key='access_token', value=access_token, httponly=True, domain='localhost', path='/')
                return response
            else:
                return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


####