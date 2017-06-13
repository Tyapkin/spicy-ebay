from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import ProductListView, ProductDetailView, ProductCreatedView,\
    ProductUpdateView

urlpatterns = [
    url(r'^$', login_required(ProductListView.as_view()), name='index'),

    url(r'^product/(?P<pk>[0-9]+)/detail/$',
        login_required(ProductDetailView.as_view()), name='product_detail'),

    url(r'^product/add/$',
        login_required(ProductCreatedView.as_view()), name='create_product'),

    url(r'^product/(?P<pk>[0-9]+)/edit/$',
        login_required(ProductUpdateView.as_view()), name='product_edit')
]
