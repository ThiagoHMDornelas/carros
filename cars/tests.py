from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from cars.forms import CarModelForm
from cars.models import Brand, Car, CarInventory


class BrandModelTest(TestCase):
    def test_str_retorna_nome(self):
        brand = Brand.objects.create(name='Toyota')
        self.assertEqual(str(brand), 'Toyota')


class CarModelTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Toyota')

    def test_str_retorna_modelo(self):
        car = Car.objects.create(model='Corolla', brand=self.brand)
        self.assertEqual(str(car), 'Corolla')


class CarInventorySignalTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Toyota')

    def test_inventario_criado_ao_salvar(self):
        Car.objects.create(model='Corolla', brand=self.brand, value=100000)
        inventory = CarInventory.objects.latest('id')
        self.assertEqual(inventory.cars_count, 1)
        self.assertEqual(inventory.cars_value, 100000)

    def test_inventario_atualizado_ao_deletar(self):
        car = Car.objects.create(model='Corolla', brand=self.brand, value=100000)
        car.delete()
        inventory = CarInventory.objects.latest('id')
        self.assertEqual(inventory.cars_count, 0)
        self.assertEqual(inventory.cars_value, 0)

    def test_bio_padrao_quando_nao_informada(self):
        car = Car.objects.create(model='Corolla', brand=self.brand)
        self.assertEqual(car.bio, 'Descrição deste carro ainda não foi informada!')


class CarModelFormTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Toyota')

    def test_valor_minimo_valido(self):
        form = CarModelForm(data={
            'model': 'Corolla',
            'brand': self.brand.id,
            'factory_year': 2020,
            'value': 20000,
        })
        self.assertTrue(form.is_valid())

    def test_valor_abaixo_do_minimo(self):
        form = CarModelForm(data={
            'model': 'Corolla',
            'brand': self.brand.id,
            'factory_year': 2020,
            'value': 19999,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('value', form.errors)

    def test_ano_fabricacao_invalido(self):
        form = CarModelForm(data={
            'model': 'Corolla',
            'brand': self.brand.id,
            'factory_year': 1969,
            'value': 20000,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('factory_year', form.errors)


class CarViewsTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Toyota')
        self.car = Car.objects.create(model='Corolla', brand=self.brand, value=100000)
        self.user = User.objects.create_user(username='usuario', password='SenhaForte123')

    def test_home_redireciona_para_lista(self):
        response = self.client.get('/')
        self.assertRedirects(response, reverse('lista_carros'))

    def test_lista_de_carros_e_publica(self):
        response = self.client.get(reverse('lista_carros'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Corolla')

    def test_detalhe_do_carro(self):
        response = self.client.get(reverse('detalhe_carro', args=[self.car.pk]))
        self.assertEqual(response.status_code, 200)

    def test_cadastro_exige_login(self):
        response = self.client.get(reverse('novo_carro'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_cadastro_autenticado(self):
        self.client.login(username='usuario', password='SenhaForte123')
        response = self.client.get(reverse('novo_carro'))
        self.assertEqual(response.status_code, 200)
