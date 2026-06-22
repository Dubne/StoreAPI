from django.db import models
from ..categories.models import Category
from django.core.validators import MinValueValidator
class Product(models.Model):
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
