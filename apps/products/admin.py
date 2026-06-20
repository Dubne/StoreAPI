from django.contrib import admin
from ..products.models import Product

class InventoryAmountFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory filter'

    def lookups(self, request, model_admin):
        return (
            ('few', 'less than 10'),
            ('enough', 'more than 10')
        )
    def queryset(self, request, queryset):
        
        if self.value() == 'few':
            return queryset.filter(inventory__lt=10)
        
        if self.value() == 'enough':
            return queryset.filter(inventory__gte=10)
        
        return queryset

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title','category__title']
    list_filter = [InventoryAmountFilter]

