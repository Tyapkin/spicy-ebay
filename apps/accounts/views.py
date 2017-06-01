from django.shortcuts import render
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.base import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Credentials


class UserSettingsView(DetailView):
    model = Credentials
    template_name = 'profile_settings.html'
    context_object_name = 'accounts'

