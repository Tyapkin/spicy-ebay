from django.test import TestCase
from django.contrib.auth.models import User

from .models import Product
from apps.accounts.models import Credentials


def create_test_client():
    test_user = User.objects.create_user('test_user', 'test@test.loc')
    test_client = Credentials.objects.create(user=test_user)
    return test_client


def create_test_product(client):
    product = Product.objects.create(
        owner=client,
        product_id='123456789012',
        qty=1
    )
    return product


class ProductModelTests(TestCase):

    def test_in_stock(self):
        """
        in_stock must take a False if the field qty <= 0,
        and must accept a True if qty > 0
        """
        client = create_test_client()
        product = create_test_product(client)
        self.assertIs(product.in_stock, True)
