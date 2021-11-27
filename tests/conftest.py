import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def payload():
    return {'title': 'Apple Iphone 13', 'description': 'крутотень', 'price': 150000}


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make('Product', **kwargs)
    return factory
