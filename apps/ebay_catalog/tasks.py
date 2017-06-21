from settings.celery import app
from .models import Product
from apps.accounts.models import Credentials
from .ebay import GetSingleItem
from pprint import pprint


def get_clients():
    return Credentials.objects.all()


@app.task
def auto_update_all_products():
    clients = get_clients()

    for client in clients:
        call = GetSingleItem(client.app_id)
        products_ids = [p['product_id'] for p in client.product_set.all().values()]
        for pid in products_ids:
            item = call.get_product(pid)
            pprint(item)
