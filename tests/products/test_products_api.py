# def test_dummy():
#     assert True
import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse

from product.models import Product


def test_sample_view(client):
    url = reverse('sample') #api/v1/test/
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['status'] == 'OK!'


@pytest.mark.django_db
def test_products_list(client, product_factory):
    #create, list - list (products-list)
    #retrieve, update, partial_update, destroy - detail (products-detail)
    url = reverse('products-list')
    # Product.objects.bulk_create(
    #     [
    #         Product(title='Apple Iphone12', description='Крутой телефон', price=100000),
    #         Product(title='Samsung S21', description='Крутой телефон', price=65000)
    #     ]
    # )
    products = product_factory(_quantity=2)
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_products_details(client, product_factory):
    #create, list - list (products-list)
    #retrieve, update, partial_update, destroy - detail (products-detail)
    # Product.objects.bulk_create(
    #     [
    #         Product(title='Apple Iphone12', description='Крутой телефон', price=100000),
    #         Product(title='Samsung S21', description='Крутой телефон', price=65000)
    #     ]
    # )
    product_factory(_quantity=2)
    product1 = Product.objects.first()
    url = reverse('products-detail', args=(product1.id, ))
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == product1.id
    assert response.data['title'] == product1.title
    assert response.data['price'] == str(product1.price)


#пытается создать продукт анонимный пользователь
@pytest.mark.django_db
def test_create_by_anonymous_user(client):
    payload = {'title': 'Xiaomi mi11',
               'description': 'Самый лучший телефон',
               'price': 40000}
    url = reverse('products-list')
    res = client.post(url, data=payload)
    assert res.status_code == 401


#пытается создать обычный пользователь
@pytest.mark.django_db
def test_create_by_simple_user(client):
    payload = {'title': 'Xiaomi mi11',
               'description': 'Самый лучший телефон',
               'price': 40000}
    user = User.objects.create_user('user1', 'user1@gmail.com', 'qwerty', is_active=True)
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    url = reverse('products-list')
    res = client.post(url, data=payload)
    assert res.status_code == 403


#пытается создать админ
@pytest.mark.django_db
def test_create_by_admin_user(client):
    payload = {'title': 'Xiaomi mi11',
               'description': 'Самый лучший телефон',
               'price': 40000}
    admin = User.objects.create_superuser('user21', 'user2@gmail.com', 'qwerty')
    token = Token.objects.create(user=admin)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    url = reverse('products-list')
    res = client.post(url, data=payload)
    assert res.status_code == 201
    assert res.data['title'] == payload['title']


@pytest.mark.django_db
def test_create_without_price(client):
    payload = {'title': 'Xiaomi mi11',
               'description': 'Самый лучший телефон'}
    admin = User.objects.create_superuser('user21', 'user2@gmail.com', 'qwerty')
    token = Token.objects.create(user=admin)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    url = reverse('products-list')
    res = client.post(url, data=payload)
    assert res.status_code == 400
    assert 'price' in res.data


@pytest.mark.parametrize(
    ['price', 'status'],
    (
        (-100, 400),
        (20000, 201),
        (20000000000000, 400)
    )
)
@pytest.mark.django_db
def test_create_with_different_prices(client, price, status):
    payload = {'title': 'Xiaomi mi11',
               'description': 'Самый лучший телефон',
               'price': price}
    admin = User.objects.create_superuser('user21', 'user2@gmail.com', 'qwerty')
    token = Token.objects.create(user=admin)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    url = reverse('products-list')
    res = client.post(url, data=payload)
    assert res.status_code == status
