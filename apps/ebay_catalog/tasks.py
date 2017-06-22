from settings.celery import app
from apps.accounts.models import Credentials
from .ebay import GetSingleItem


def get_clients():
    return Credentials.objects.all()


@app.task
def auto_update_all_products():
    clients = get_clients()
    success_updated = 0
    not_updated = 0

    for client in clients:
        call = GetSingleItem(client.app_id)
        products_ids = [p['product_id'] for p in client.product_set.all().values()]
        for pid in products_ids:
            item = call.get_product(pid)
            try:
                for e in client.product_set.filter(product_id=pid):
                    e.rating = item['Seller']['FeedbackScore']
                    e.price = item['CurrentPrice']['Value']
                    e.qty = item['Quantity']
                    e.save()
                success_updated += 1
            except Exception as e:
                not_updated += 1
                continue
    print('Successfully updated: {}; Not updated: {}'.format(success_updated, not_updated))
