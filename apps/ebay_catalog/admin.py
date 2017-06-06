from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['upc', 'owner', 'rating', 'date_updated']
    search_fields = ['upc', 'name']
    ordering = ['rating', 'qty', 'date_updated']

admin.site.register(Product, ProductAdmin)
