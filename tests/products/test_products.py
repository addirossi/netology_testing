# def square(number):
#     return number ** 2
#
#
# assert square(10) == 90

# names = ['Vika', 'Lena', 'Olya']
#
# assert 'Rita' in names

# def test_dummy():
#     assert True
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from product.models import Product


def test_sample_view(client):
    url = reverse('sample')
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['status'] == 'OK!'


@pytest.mark.django_db
def test_create_product_as_anonymous(client):
    data = {'title': 'Samsung Galaxy S21',
            'description': 'Крутота!',
            'price': 60000}
    url = reverse('create-product')
    response = client.post(url, data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_product_as_simple_user(client):
    data = {'title': 'Samsung Galaxy S21',
            'description': 'Крутота!',
            'price': 60000}
    url = reverse('create-product')
    user = User.objects.create_user('user1',
                                    'user1@gmail.com',
                                    'qwerty',
                                    is_active=True)
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    response = client.post(url, data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_product_as_admin_user(client):
    data = {'title': 'Samsung Galaxy S21',
            'description': 'Крутота!',
            'price': 60000}
    url = reverse('create-product')
    admin = User.objects.create_superuser('user1',
                                          'user1@gmail.com',
                                          'qwerty',
                                          is_active=True)
    token = Token.objects.create(user=admin)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.data['title'] == data['title']
    assert response.data['price'] == '60000.00'


@pytest.mark.django_db
def test_create_product_without_title(client):
    data = {'description': 'Крутота!',
            'price': 60000}
    url = reverse('create-product')
    admin = User.objects.create_superuser('user1',
                                          'user1@gmail.com',
                                          'qwerty',
                                          is_active=True)
    token = Token.objects.create(user=admin)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    response = client.post(url, data)
    assert response.status_code == 400
    assert 'title' in response.data

#
# @pytest.mark.django_db
# def test_create_product_with_negative_price():
#     data = {'title': 'Samsung Galaxy S21',
#             'description': 'Крутота!',
#             'price': -100}
#     client = APIClient()
#     url = reverse('create-product')
#     admin = User.objects.create_superuser('user1',
#                                           'user1@gmail.com',
#                                           'qwerty',
#                                           is_active=True)
#     token = Token.objects.create(user=admin)
#     client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
#     response = client.post(url, data)
#     assert response.status_code == 400
#     assert 'price' in response.data
#
#
# @pytest.mark.django_db
# def test_create_product_with_empty_price():
#     data = {'title': 'Samsung Galaxy S21',
#             'description': 'Крутота!',
#             'price': ''}
#     client = APIClient()
#     url = reverse('create-product')
#     admin = User.objects.create_superuser('user1',
#                                           'user1@gmail.com',
#                                           'qwerty',
#                                           is_active=True)
#     token = Token.objects.create(user=admin)
#     client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
#     response = client.post(url, data)
#     assert response.status_code == 400
#     assert 'price' in response.data
#
#
# @pytest.mark.django_db
# def test_create_product_with_normal_price():
#     data = {'title': 'Samsung Galaxy S21',
#             'description': 'Крутота!',
#             'price': '80000.00'}
#     client = APIClient()
#     url = reverse('create-product')
#     admin = User.objects.create_superuser('user1',
#                                           'user1@gmail.com',
#                                           'qwerty',
#                                           is_active=True)
#     token = Token.objects.create(user=admin)
#     client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
#     response = client.post(url, data)
#     assert response.status_code == 201
#     assert response.data['price'] == data['price']
#
#
# @pytest.mark.django_db
# def test_create_product_with_giant_price():
#     data = {'title': 'Samsung Galaxy S21',
#             'description': 'Крутота!',
#             'price': '800000000000000000.00'}
#     client = APIClient()
#     url = reverse('create-product')
#     admin = User.objects.create_superuser('user1',
#                                           'user1@gmail.com',
#                                           'qwerty',
#                                           is_active=True)
#     token = Token.objects.create(user=admin)
#     client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
#     response = client.post(url, data)
#     assert response.status_code == 400
#     assert 'price' in response.data


@pytest.mark.django_db
@pytest.mark.parametrize(
    ['price', 'status'],
    (
        ('-100', 400),
        ('', 400),
        ('80000.00', 201),
        ('1000000000000000000', 400)
    )
)
def test_create_product_with_price(client, price, status):
    data = {'title': 'Samsung Galaxy S21',
            'description': 'Крутота!',
            'price': price}
    url = reverse('create-product')
    admin = User.objects.create_superuser('user1',
                                          'user1@gmail.com',
                                          'qwerty',
                                          is_active=True)
    token = Token.objects.create(user=admin)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    response = client.post(url, data)
    assert response.status_code == status


@pytest.mark.django_db
def test_products_list(client, product_factory):
    url = reverse('products-list')
    product_factory(_quantity=3)
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3


@pytest.mark.django_db
def test_products_list_2(client, product_factory):
    url = reverse('products-list')
    product_factory(title='Apple Iphone13')
    response = client.get(url)
    assert response.status_code == 200
    assert response.data[0]['title'] == 'Apple Iphone13'
