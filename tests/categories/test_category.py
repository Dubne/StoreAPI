import pytest
from rest_framework import status

from apps.categories.models import Category


@pytest.mark.django_db
def test_everyone_can_get_categories(client):
    Category.objects.create(
        title="Phones",
        description="test description"
    )

    response = client.get("/api/categories/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_everyone_can_get_single_category(client, category):
    response = client.get(
        f"/api/categories/{category.id}/"
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_admin_can_create_category(client, admin_user):
    client.force_authenticate(user=admin_user)

    response = client.post(
        "/api/categories/",
        {
            "title": "Phones",
            "description": "test description"
        },
        format="json"
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Category.objects.count() == 1


@pytest.mark.django_db
def test_user_cannot_create_category(client, user):
    client.force_authenticate(user=user)

    response = client.post(
        "/api/categories/",
        {
            "title": "Phones",
            "description": "test description"
        },
        format="json"
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_delete_category(client, admin_user, category):
    client.force_authenticate(user=admin_user)

    response = client.delete(
        f"/api/categories/{category.id}/"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Category.objects.count() == 0


@pytest.mark.django_db
def test_user_cannot_delete_category(client, user, category):
    client.force_authenticate(user=user)

    response = client.delete(
        f"/api/categories/{category.id}/"
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN