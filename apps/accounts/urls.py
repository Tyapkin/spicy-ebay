from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from .views import UserSettingsView, CredentialsVeiw, CredentialsAddView, CredentialsEditView

urlpatterns = [
    url(r'^settings/(?P<pk>[0-9]+)/$',
        login_required(UserSettingsView.as_view()), name='settings'),

    url(r'^settings/credentials/(?P<pk>[0-9]+)/$',
        CredentialsVeiw.as_view(), name='credentials'),

    url(r'^settings/credentials/add/$',
        CredentialsAddView.as_view(), name='add_credentials'),

    url(r'^settings/credentials/edit/(?P<pk>[0-9]+)/$',
        CredentialsEditView.as_view(), name='edit_credentials'),

    url(r'^', include('registration.backends.hmac.urls')),
]
