import pytest
from rest_framework import status

from apps.products.models import Product


@pytest.mark.django_db
def test_everyone_can_get_products(client):
    response = client.get("/api/products/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_everyone_can_get_single_product(client, product):
    response = client.get(
        f"/api/products/{product.id}/"
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_admin_can_create_product(client, admin_user, category):
    client.force_authenticate(user=admin_user)

    response = client.post(
        "/api/products/",
        {
            "title": "Macbook",
            "description": "Apple laptop",
            "price": "1500",
            "inventory": 15,
            "category_id": category.id,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_user_cannot_create_product(client, user, category):
    client.force_authenticate(user=user)

    response = client.post(
        "/api/products/",
        {
            "title": "Macbook",
            "description": "Apple laptop",
            "price": "1500",
            "inventory": 15,
            "category_id": category.id,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_delete_product(client, admin_user, product):
    client.force_authenticate(user=admin_user)

    response = client.delete(
        f"/api/products/{product.id}/"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Product.objects.count() == 0


@pytest.mark.django_db
def test_user_cannot_delete_product(client, user, product):
    client.force_authenticate(user=user)

    response = client.delete(
        f"/api/products/{product.id}/"
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_update_product(client, admin_user, product):
    client.force_authenticate(user=admin_user)

    response = client.patch(
        f"/api/products/{product.id}/",
        {
            "price": "2000"
        },
        format="json",
    )

    product.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert str(product.price) == "2000.00"


@pytest.mark.django_db
def test_user_cannot_update_product(client, user, product):
    client.force_authenticate(user=user)

    response = client.patch(
        f"/api/products/{product.id}/",
        {
            "price": "2000"
        },
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

