from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .serializers import SignupSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class SignupView(APIView):
    """
    Endpoint para cadastro de novos usuários.
    Requer os campos 'email', 'nome', 'password' e 'password2'.
    Retorna os dados do usuário criado.
    """
    @swagger_auto_schema(
        operation_summary="Cadastro de Usuário",
        operation_description="Cadastra um novo usuário no sistema.",
        request_body=SignupSerializer,
        responses={
            201: "Usuário criado com sucesso.",
            400: "Erro de validação."
        }
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Endpoint para login de usuários.
    Requer os campos 'email' e 'password'.
    Retorna tokens JWT ('access' e 'refresh') em caso de sucesso.
    """
    @swagger_auto_schema(
        operation_summary="Login de Usuário",
        operation_description="Autentica um usuário e retorna tokens JWT.",
        request_body=LoginSerializer,
        responses={
            200: "Login bem-sucedido. Retorna tokens JWT.",
            400: "Erro de validação.",
            401: "Credenciais inválidas."
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    """
    Endpoint protegido para obter os dados do usuário autenticado.
    Requer um token JWT válido no header 'Authorization'.
    Retorna os campos 'email' e 'nome' do usuário.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Dados do Usuário Autenticado",
        operation_description="Retorna os dados do usuário autenticado.",
        responses={
            200: "Dados do usuário retornados com sucesso.",
            401: "Não autorizado. Token JWT inválido ou ausente."
        }
    )
    def get(self, request):
        user = request.user
        return Response({
            'email': user.email,
            'nome': user.nome,
        }, status=status.HTTP_200_OK)