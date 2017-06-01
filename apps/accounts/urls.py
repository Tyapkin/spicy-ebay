from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from .views import UserSettingsView

urlpatterns = [
    url(r'^settings/(?P<pk>[0-9]+)/$', login_required(UserSettingsView.as_view()),
        name='settings'),
    url(r'^', include('registration.backends.hmac.urls')),
]
