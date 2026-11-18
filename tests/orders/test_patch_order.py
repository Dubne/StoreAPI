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


@pytest.mark.django_db
def test_admin_cancelling_order_restores_inventory(
        client,
        admin_user,
        user,
        product
):
    order = Order.objects.create(user=user)
    OrderItem.objects.create(
        order=order,
        product=product,
        amount=3
    )
    product.inventory = 7
    product.save(update_fields=["inventory"])

    client.force_authenticate(user=admin_user)

    response = client.patch(
        f"/api/orders/{order.id}/",
        {"status": "cancelled"},
        format="json"
    )

    order.refresh_from_db()
    product.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert order.status == "cancelled"
    assert product.inventory == 10


@pytest.mark.django_db
def test_delivered_order_cannot_be_cancelled(
        client,
        admin_user,
        user
):
    order = Order.objects.create(
        user=user,
        status=Order.Status.DELIVERED
    )

    client.force_authenticate(user=admin_user)

    response = client.patch(
        f"/api/orders/{order.id}/",
        {"status": "cancelled"},
        format="json"
    )

    order.refresh_from_db()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert order.status == Order.Status.DELIVERED