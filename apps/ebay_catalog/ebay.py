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

SELECTORS = {
    # getSingleItem
    'details': 'Details',
    'description': 'Description',
    'itemspecifics': 'ItemSpecifics',
    'shippingcost': 'ShippingCosts',
    'variations': 'Variations',
    # findItemsByProduct
    'aspecthistogram': 'AspectHistogram',
    'categoryhistogram': 'CategoryHistogram',
    'conditionhistogram': 'ConditionHistogram',
    'galleryinfo': 'GalleryInfo',
    'pic_url_large': 'PictureURLLarge',
    'sellerinfo': 'SellerInfo',
    'storeinfo': 'StoreInfo',
    'unitpriceinfo': 'UnitPriceInfo'
}


class GetProductByUPC:
    def __init__(self, app_id, id_type='upc', endpoint=settings.PRODUCTION_ENDPOINT, selector='sellerinfo'):
        self.app_id = app_id
        self.endpoint = endpoint
        self.product_id_type = TYPES[id_type]
        self.test_product_id = '858978005271'
        self.selector = selector
        self.session = requests.Session()

    def get_payload(self):
        payload = {
            'OPERATION-NAME': 'findItemsByProduct',
            'SERVICE-VERSION': '1.0.0',
            'SECURITY-APPNAME': self.app_id,
            'RESPONSE-DATA-FORMAT': 'JSON',
            'REST-PAYLOAD': None,
            'outputSelector': SELECTORS[self.selector],
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
                for i in range(0, int(content['searchResult'][0]['@count'])):
                    try:
                        results.append({
                            'upc': product_id,
                            'itemId': content['searchResult'][0]['item'][i]['itemId'][0]
                        })
                    except Exception as e:
                        print(e)
                        continue
                return results
            else:
                print(content['errorMessage'])
        else:
            return 'Error'


class GetSingleItem:
    def __init__(self, app_id, endpoint='http://open.api.ebay.com/shopping', selector='details'):
        self.app_id = app_id
        self.endpoint = endpoint
        self.test_product_id = '322544108389'
        self.session = requests.Session()
        self.selector = SELECTORS[selector]

    def get_payload(self, item_id):
        payload = {
            'callname': 'GetSingleItem',
            'responseencoding': 'JSON',
            'appid': self.app_id,
            'siteid': '77',
            'version': '967',
            'ItemID': item_id,
            'IncludeSelector': self.selector
        }
        return payload

    def get_product(self, item_id):
        payload = self.get_payload(item_id)
        session = requests.Session()
        resp = session.request('GET', self.endpoint, params=payload)

        if resp.status_code == requests.codes.ok:
            product = json.loads(resp.text)
            if product['Ack'] == STATUS:
                return product['Item']
            else:
                print('{}: {} Classification: {}'.format(product['Errors'][0]['SeverityCode'],
                                                         product['Errors'][0]['ShortMessage'],
                                                         product['Errors'][0]['ErrorClassification']))
                return 'Error'
        else:
            return 'Error'


# TODO: delete this
from apps.accounts.models import Credentials

client = Credentials.objects.get(user__username='alex')

call = GetProductByUPC(client.app_id)

call2 = GetSingleItem(client.app_id)

from pprint import pprint