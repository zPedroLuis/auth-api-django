from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class AuthAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='usuario@teste.com',
            nome='Usuário Teste',
            password='senha1234'
        )

    def test_signup(self):
        url = reverse('signup')
        data = {
            'email': 'novousuario@teste.com',
            'nome': 'Novo Usuário',
            'password': 'senha1234',
            'password2': 'senha1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_login(self):
        url = reverse('login')
        data = {
            'email': 'usuario@teste.com',
            'password': 'senha1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data) 

    def test_me_authenticated(self):        
        url = reverse('me')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'usuario@teste.com')

    def test_me_unauthenticated(self):
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)