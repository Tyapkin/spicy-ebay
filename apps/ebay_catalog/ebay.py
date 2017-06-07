from django.conf import settings
import requests
import json
from datetime import date


TYPES = {
    'upc': 'UPC',
    'ean': 'EAN',
    'isbn': 'ISBN'
}

STATUS = 'Success'


class GetProductByUPC:
    def __init__(self, app_id, id_type='upc', endpoint=settings.PRODUCTION_ENDPOINT):
        self.app_id = app_id
        self.endpoint = endpoint
        self.product_id_type = TYPES[id_type]
        self.test_product_id = '858978005271'
        self.session = requests.Session()

    def get_payload(self):
        payload = {
            'OPERATION-NAME': 'findItemsByProduct',
            'SERVICE-VERSION': '1.0.0',
            'SECURITY-APPNAME': self.app_id,
            'RESPONSE-DATA-FORMAT': 'JSON',
            'REST-PAYLOAD': None,
            'productId.@type': self.product_id_type,
            'productId': self.test_product_id
        }
        return payload

    def get_test_product(self):
        payload = self.get_payload()
        response = self.session.request('GET', self.endpoint, params=payload)
        # content = json.loads(response.text)['findItemsByProductResponse'][0]['searchResult'][0]['item'][0]
        content = json.loads(response.text)
        return content

    def get_product(self, product_id):
        payload = self.get_payload()
        payload['productId'] = product_id
        response = self.session.request('GET', self.endpoint, params=payload)

        if response.status_code == requests.codes.ok:
            content = json.loads(response.text)['findItemsByProductResponse'][0]
            if content['ack'][0] == STATUS:
                results = []
                for i in range(0, len(content['searchResult'][0]['item'])):
                    try:
                        results.append({
                            'upc': content['searchResult'][0]['item'][i]['itemId'][0],
                            'img': content['searchResult'][0]['item'][i]['galleryURL'][0],
                            'rating': content['searchResult'][0]['item'][i]['sellerInfo'][0]['feedbackScore'][0],
                            'price': content['searchResult'][0]['item'][i]['currentPrice'][0]['__value__'],
                            'title': content['searchResult'][0]['item'][i]['title'][0],
                            'in_stock': True if content['searchResult'][0]['item'][i]['sellingStatus'][0]['sellingState'][0] == 'Active' else False,
                            # 'qty': 0,
                            # 'weight': 0,
                            # 'dims': 0,
                            'date_updated': date.today()
                        })
                    except Exception as e:
                        print(e)
                        pass
                return results
            else:
                print(content['errorMessage'])
        else:
            return 'Error'
