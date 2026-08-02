import pytest
from apps.orders.models import Order, OrderItem
from rest_framework import status

@pytest.mark.django_db
def test_admin_can_change_order_status(
        client,
        admin_user
):

    order = Order.objects.create(user=admin_user)

    client.force_authenticate(user=admin_user)

    response = client.patch(
        f"/api/orders/{order.id}/",
        {"status": "cancelled"},
        format="json"
    )

    order.refresh_from_db()

    print(response.status_code)
    print(response.data)

    assert response.status_code == status.HTTP_200_OK
    assert order.status == "cancelled"


@pytest.mark.django_db
def test_user_cannot_change_order_status(
        client,
        user
):

    order = Order.objects.create(user=user)

    client.force_authenticate(user=user)

    response = client.patch(
        f"/api/orders/{order.id}/",
        {"status": "CANCELLED"},
        format="json"
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN