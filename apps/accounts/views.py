from django.shortcuts import render
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.base import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Credentials


class UserSettingsView(DetailView):
    model = User
    template_name = 'profile_settings.html'
    context_object_name = 'profile'


class CredentialsVeiw(DetailView):
    context_object_name = 'credentials'
    template_name = 'credentials_detail.html'

    def get_object(self, queryset=None):
        try:
            return Credentials.objects.get(user=self.request.user)
        except Credentials.DoesNotExist:
            return

    def get_context_data(self, **kwargs):
        context = super(CredentialsVeiw, self).get_context_data(**kwargs)
        if self.object:
            context['is_empty'] = False
        else:
            context['is_empty'] = True
        return context


