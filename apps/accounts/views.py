from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
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


class CredentialsAddView(CreateView):
    model = Credentials
    template_name = 'credentials_form.html'
    fields = ['runame', 'app_id', 'dev_id', 'cert_id']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CredentialsAddView, self).form_valid(form)


class CredentialsEditView(UpdateView):
    model = Credentials
    fields = ['runame', 'app_id', 'dev_id', 'cert_id']


