from django.contrib import admin
from ..reviews.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'mark']
    list_filter = ['product', 'user']
