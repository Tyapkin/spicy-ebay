from django.db import models
from apps.accounts.models import Credentials


class Product(models.Model):
    owner = models.ForeignKey(Credentials, on_delete=models.CASCADE)
    upc = models.CharField(max_length=12)
    product_id = models.CharField(max_length=12, null=True)
    image = models.URLField(blank=True)
    rating = models.FloatField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True)
    in_stock = models.BooleanField(default=False)
    qty = models.IntegerField(blank=True, null=True, default=0)
    weight = models.FloatField(blank=True, null=True, default=0.0)
    length = models.FloatField(blank=True, null=True, default=0.0)
    width = models.FloatField(blank=True, null=True, default=0.0)
    height = models.FloatField(blank=True, null=True, default=0.0)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['rating', 'qty', 'date_updated']

    def __str__(self):
        return '{}: UPC: {}; Product ID: {}'.format(self.name, self.upc, self.product_id)
