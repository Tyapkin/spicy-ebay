from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Credentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # ebay api
    runame = models.CharField('ruName', max_length=254, unique=True)
    app_id = models.CharField('app id', max_length=254, unique=True)
    dev_id = models.CharField('dev id', max_length=254, blank=True, default='')
    cert_id = models.CharField('cert id', max_length=254, blank=True, default='')

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def get_absolute_url(self):
        return reverse('credentials')
