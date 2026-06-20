from django.db import models
from ..users.models import User
from ..products.models import Product
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    on_created = models.DateTimeField(auto_now_add=True)
    class Status(models.TextChoices):
        PENDING = 'pending',
        PAID = 'paid',
        SHIPPED = 'shipped',
        DELIVERED = 'delivered',
        CANCELLED = 'cancelled'
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

   

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    amount = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

   