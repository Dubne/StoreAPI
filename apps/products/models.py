from django.db import models
from ..categories.models import Category
class Product(models.Model):
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
