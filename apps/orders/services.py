from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem
from django.db import transaction
from django.db.models import Sum
from apps.products.models import Product

@transaction.atomic
def create_order(user, data):
    items = data["items"]
    aggregated = aggregate_items(items)
    products = {
        product.pk: product
        for product in Product.objects.select_for_update().filter(
            pk__in=aggregated.keys()
        )
    }

    check_inventory(aggregated, products)
    order = Order.objects.create(user=user)

    for product_id, amount in aggregated.items():
        product = products[product_id]
        OrderItem.objects.create(
            order=order,
            product=product,
            amount=amount
        )
        product.inventory -= amount
        product.save(update_fields=["inventory"])

    return order

def return_inventory(order):
    totals = order.items.values("product_id").annotate(
        amount=Sum("amount")
    )
    products = {
        product.pk: product
        for product in Product.objects.select_for_update().filter(
            pk__in=[item["product_id"] for item in totals]
        )
    }

    for item in totals:
        product = products[item["product_id"]]
        product.inventory += item["amount"]
        product.save(update_fields=["inventory"])

@transaction.atomic
def cancel_order(order):
    order = Order.objects.select_for_update().get(pk=order.pk)

    if order.status == Order.Status.DELIVERED:
        raise ValidationError("Delivered orders cannot be cancelled")
    if order.status == Order.Status.CANCELLED:
        raise ValidationError("This order is already cancelled")

    order.status = Order.Status.CANCELLED
    return_inventory(order)
    order.save(update_fields=["status"])
    return order

def aggregate_items(items):
    aggregated = {}
    for item in items:
        product = item["product"]
        amount = item["amount"]
        if amount < 1:
            raise ValidationError("Item amount must be at least 1.")
        aggregated[product.pk] = aggregated.get(product.pk, 0) + amount
    return aggregated

def check_inventory(aggregated, products):
    for product_id, quantity in aggregated.items():
        product = products.get(product_id)
        if product is None:
            raise ValidationError("One or more products do not exist.")
        if quantity > product.inventory:
            raise ValidationError(
                f"There are not enough {product.title} in stock."
            )
        
    



