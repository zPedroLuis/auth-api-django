from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer para cadastro de novos usuários.
    Requer os campos 'email', 'nome', 'password' e 'password2'.
    A senha deve ser válida e as senhas devem coincidir.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        help_text="Senha do usuário (deve ser válida e segura)."
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Confirmação da senha. Deve ser igual ao campo 'password'."
    )

    class Meta:
        model = User
        fields = ['email', 'nome', 'password', 'password2']
        extra_kwargs = {
            'email': {'help_text': "Endereço de email do usuário (deve ser único)."},
            'nome': {'help_text': "Nome completo do usuário."},
        }

    def validate(self, attrs):
        """
        Valida se as senhas coincidem.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return attrs

    def create(self, validated_data):
        """
        Cria um novo usuário no sistema.
        """
        validated_data.pop('password2')  # Remove o campo 'password2'
        user = User.objects.create_user(
            email=validated_data['email'],
            nome=validated_data['nome'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer para login de usuários.
    Requer os campos 'email' e 'password'.
    Retorna tokens JWT ('access' e 'refresh') em caso de sucesso.
    """
    email = serializers.EmailField(
        required=True,
        help_text="Endereço de email do usuário."
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        help_text="Senha do usuário."
    )