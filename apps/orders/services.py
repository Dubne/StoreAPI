from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem
from django.db import transaction

@transaction.atomic
def create_order(user, data):
    items = data["items"]
    check_inventory(items)
    total_price = calculate_total_price(items)
    order = Order.objects.create(user=user, total_price=total_price)
    create_order_items(order, items)
    reduce_inventory(order)
    return order

def create_order_items(order, items):

    for item in items:

        OrderItem.objects.create(
            order=order,
            product=item["product"],
            quantity=item["quantity"]
        )

def return_inventory(order):
    for item in order.items.all():
        product = item.product
        product.inventory += item.amount
        product.save() 

@transaction.atomic
def cancel_order(order):
    if order.status == "DELIVERED":
        raise ValidationError("Delivered orders cannot be cancelled")
    
    order.status = "CANCELLED"
    return_inventory(order)
    order.save()

def reduce_inventory(order):

    for item in order.items.all():
        product = item.product
        product.inventory -= item.amount
        product.save()


def check_inventory(items):
    for item in items:
        product = item["product"]
        quantity = item['amount']
        if quantity > product.inventory:
            raise ValidationError(f"There are not enough {product.title} in stock.")
        
    


def calculate_total_price(items):
    total_price = 0
    for item in items:
        total_price += item.product.price * item.amount
    return total_price


