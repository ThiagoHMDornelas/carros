from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountsViewsTest(TestCase):
    def test_registro_cria_usuario(self):
        response = self.client.post(reverse('registro'), {
            'username': 'novousuario',
            'password1': 'SenhaForte123',
            'password2': 'SenhaForte123',
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='novousuario').exists())

    def test_login_valido(self):
        User.objects.create_user(username='usuario', password='SenhaForte123')
        response = self.client.post(reverse('login'), {
            'username': 'usuario',
            'password': 'SenhaForte123',
        })
        self.assertRedirects(response, reverse('lista_carros'))

    def test_login_invalido(self):
        response = self.client.post(reverse('login'), {
            'username': 'nao_existe',
            'password': 'errada',
        })
        self.assertEqual(response.status_code, 200)
