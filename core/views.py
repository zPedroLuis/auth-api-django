from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import SignupSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Cadastro
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                # Gerar tokens JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user = request.user
        return Response({
            'email': user.email,
            'nome': user.nome,
        })