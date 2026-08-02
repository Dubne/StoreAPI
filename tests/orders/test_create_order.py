import pytest
from apps.orders.models import Order, OrderItem


@pytest.mark.django_db
def test_authenticated_user_can_create_order(
        client,
        user,
        product
):

    client.force_authenticate(user=user)

    data = {
        "items": [
            {
                "product": product.id,
                "amount": 2
            }
        ]
    }

    response = client.post(
        "/api/orders/",
        data,
        format="json"
    )

    product.refresh_from_db()

    assert response.status_code == 201
    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 1
    assert product.inventory == 8


@pytest.mark.django_db
def test_anonymous_user_cannot_create_order(
        client,
        product
):

    data = {
        "items": [
            {
                "product": product.id,
                "amount": 2
            }
        ]
    }

    response = client.post(
        "/api/orders/",
        data,
        format="json"
    )

    assert response.status_code == 401
    assert Order.objects.count() == 0

@pytest.mark.django_db
def test_order_is_not_created_when_inventory_is_insufficient(
        client,
        user,
        product
):

    client.force_authenticate(user=user)

    data = {
        "items": [
            {
                "product": product.id,
                "amount": 20
            }
        ]
    }

    response = client.post(
        "/api/orders/",
        data,
        format="json"
    )

    product.refresh_from_db()

    assert response.status_code == 400
    assert Order.objects.count() == 0
    assert product.inventory == 10

import pytest

from apps.orders.models import Order


@pytest.mark.django_db
def test_total_price_is_calculated_correctly(
        client,
        user,
        product
):

    client.force_authenticate(user=user)

    data = {
        "items": [
            {
                "product": product.id,
                "amount": 2
            }
        ]
    }

    response = client.post(
        "/api/orders/",
        data,
        format="json"
    )

    order = Order.objects.first()

    print(response.data)
    print(response.status_code)

    assert response.status_code == 201
    assert order.total_price == 200