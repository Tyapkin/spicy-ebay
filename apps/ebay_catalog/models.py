from django.db import models
from apps.accounts.models import Credentials


class Product(models.Model):
    owner = models.ForeignKey(Credentials, on_delete=models.CASCADE)
    upc = models.CharField(max_length=12)
    image = models.CharField(max_length=255, blank=True)
    rating = models.FloatField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True)
    in_stock = models.BooleanField(default=True)
    qty = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    dimensions = models.FloatField(blank=True, null=True)  # maybe needs all fields e.g. width, height etc.
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['rating', 'qty', 'date_updated']

    def __str__(self):
        return 'UPC: {} Owner: {}'.format(self.upc, self.owner)
