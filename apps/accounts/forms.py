from django.forms import ModelForm
from .models import Credentials


class CredentialsForm(ModelForm):

    class Meta:
        model = Credentials
        fields = ['runame', 'app_id', 'dev_id', 'cert_id']
