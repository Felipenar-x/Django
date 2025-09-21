from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'owner', 'quantity')
	search_fields = ('name', 'owner__username')

# Register your models here.
