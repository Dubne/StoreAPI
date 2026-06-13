from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ..orders.models import Product
from ..users.models import User

class Review(models.Model):
    review = models.CharField(max_length=255)
    mark = models.IntegerField(validators= [MinValueValidator(1) ,MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
