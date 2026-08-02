import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.products.models import Product


User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="nikita",
        password="123456",
        email="nikitkaaa123@email.com"
    )


@pytest.fixture
def category():
    return Category.objects.create(
        title="Phones"
    )


@pytest.fixture
def product(category):
    return Product.objects.create(
        title="Iphone",
        description="test description",
        price=100,
        inventory=10,
        category=category
    )
@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username="admin",
        password="123456",
        is_staff=True
    )


@pytest.fixture
def another_user():
    return User.objects.create_user(
        username="another",
        password="123456"
    )