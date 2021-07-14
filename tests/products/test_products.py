# from django.urls import reverse
# from rest_framework.test import APIClient

#
# def test_request():
#     client = APIClient()
#     url = reverse('test-view')
#     response = client.get(url)
#     assert response.status_code == 200
#     assert response.data['status'] == 'Ok'
from decimal import Decimal

# import pytest
#
# from product.models import Product
#
#
# @pytest.mark.django_db
# def test_product_db():
#     product = Product.objects.create(title='Apple Iphone 12',
#                                      description='Крутой телефон',
#                                      price=100000)
#     assert product.id
#     assert product.title == 'Apple Iphone 12'
#     assert product.price == 100000
from django.contrib.auth.models import User
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from product.models import Product


@pytest.mark.django_db
def test_product_create_anonymous(api_client, product_factory):
    url = reverse('product-list')
    payload = {'title': 'Apple IPhone 11 Pro',
               'description': 'Не такой крутой, как 12',
               'price': 80000}
    response = api_client.post(url, data=payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_product_list(api_client, product_factory):
    product_factory(_quantity=3, price=100000)
    url = reverse('product-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3


@pytest.mark.parametrize(
    ['price', 'expected_status'],
    (
        (-1000, 400),
        (20000, 201),
        (10000000000, 400)
    )
)
@pytest.mark.django_db
def test_create_product_with_different_prices(api_client, product_factory, price, expected_status):
    user_admin = User.objects.create_superuser(username='test', password='qwerty')
    user_token = Token.objects.create(user=user_admin)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    url = reverse('product-list')
    payload = {'title': 'Apple IMac', 'description': '...', 'price': price}
    response = api_client.post(url, data=payload)
    assert response.status_code == expected_status
