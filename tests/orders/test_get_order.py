import pytest
from apps.orders.models import Order, OrderItem
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

@pytest.mark.django_db
def test_authenticated_user_can_get_own_order(client, user, product):

    other_user = User.objects.create_user(
        username="ivan",
        password="1234567"
    )

    Order.objects.create(user=user)

    Order.objects.create(user=user)

    Order.objects.create(user=other_user)

    client.force_authenticate(user=user)
    response = client.get("/api/orders/")

    assert response.status_code == 200
    assert len(response.data["results"])

@pytest.mark.django_db
def test_admin_can_see_all_orders(
        client,
        admin_user,
        user
):

    Order.objects.create(user=user)
    Order.objects.create(user=user)
    Order.objects.create(user=admin_user)

    client.force_authenticate(user=admin_user)

    response = client.get("/api/orders/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 3


@pytest.mark.django_db
def test_unauthenticated_user_cannot_get_orders(
        client
):

    response = client.get("/api/orders/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_user_can_retrieve_his_order(
        client,
        user
):

    order = Order.objects.create(user=user)

    client.force_authenticate(user=user)

    response = client.get(
        f"/api/orders/{order.id}/"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == order.id


@pytest.mark.django_db
def test_user_cannot_retrieve_another_users_order(
        client,
        user
):

    other_user = User.objects.create_user(
        username="ivan",
        password="123456"
    )

    order = Order.objects.create(
        user=other_user
    )

    client.force_authenticate(user=user)

    response = client.get(
        f"/api/orders/{order.id}/"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND