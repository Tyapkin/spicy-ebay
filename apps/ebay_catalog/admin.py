from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['upc', 'product_id', 'owner', 'rating', 'date_updated', 'in_stock']
    list_display_links = ['upc', 'product_id']
    search_fields = ['upc', 'product_id', 'name']
    ordering = ['rating', 'qty', 'date_updated']

admin.site.register(Product, ProductAdmin)
