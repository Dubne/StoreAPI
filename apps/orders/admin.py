from django.contrib import admin
from ..orders.models import Order, OrderItem



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'on_created' ]
    search_fields = ['user', 'on_created']
    inlines = [OrderItemInline]
    

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass

