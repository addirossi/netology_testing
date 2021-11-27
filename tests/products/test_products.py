import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token

# def test_dummy():
#     assert False
from product.models import Product


def test_simple_view(client):
    url = reverse('test')
    expected_result = 'Hello world!'
    response = client.get(url)
    assert response.status_code == 200
    assert response.data == expected_result


@pytest.mark.django_db
def test_products_list(client, product_factory):
    # Product.objects.bulk_create(
    #     [
    #         Product(1, 'Apple Iphone 13', 'крутотень', 150000),
    #         Product(2, 'Samsung Galaxy S21', 'Топчик', 80000)
    #     ]
    # )
    product_factory(_quantity=2)
    url = reverse('products-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_create_product_as_anon_user(client, payload):
    url = reverse('create-product')
    response = client.post(url, payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_product_as_simple_user(client, payload):
    url = reverse('create-product')
    user1 = User.objects.create_user('user1', password='qwerty', is_active=True)
    token = Token.objects.create(user=user1)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    response = client.post(url, payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_product_as_admin_user(client, payload):
    url = reverse('create-product')
    user2 = User.objects.create_superuser('user2', password='qwerty', is_active=True)
    token = Token.objects.create(user=user2)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    response = client.post(url, payload)
    assert response.status_code == 201
    assert response.data['title'] == payload['title']


@pytest.mark.django_db
def test_create_product_without_price(client):
    payload = {'title': 'Apple Iphone 13', 'description': 'крутотень'}
    url = reverse('create-product')
    user2 = User.objects.create_superuser('user2', password='qwerty', is_active=True)
    token = Token.objects.create(user=user2)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    response = client.post(url, payload)
    assert response.status_code == 400
    assert 'price' in response.data


@pytest.mark.parametrize(
    ['price', 'status'],
    (
        (10000, 201),
        (-100, 400),
        (100000900000, 400),
        ('', 400)
    )
)
@pytest.mark.django_db
def test_create_product_with_different_prices(client, payload, price, status):
    payload['price'] = price
    url = reverse('create-product')
    user2 = User.objects.create_superuser('user2', password='qwerty', is_active=True)
    token = Token.objects.create(user=user2)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    response = client.post(url, payload)
    assert response.status_code == status


@pytest.mark.django_db
def test_delete_product_as_anon_user(client, product_factory):
    product = product_factory()
    url = reverse('delete-product', args=(product.id, ))
    response = client.delete(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_product_as_simple_user(client, product_factory):
    product = product_factory()
    url = reverse('delete-product', args=(product.id, ))
    user1 = User.objects.create_user('user1', password='qwerty', is_active=True)
    token = Token.objects.create(user=user1)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    response = client.delete(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_product_as_admin_user(client, product_factory):
    product = product_factory()
    url = reverse('delete-product', args=(product.id, ))
    user2 = User.objects.create_superuser('user2', password='qwerty')
    token = Token.objects.create(user=user2)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    response = client.delete(url)
    assert response.status_code == 204
    assert response.data is None
