from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'apps.accounts'
    verbose_name = 'accounts'

    def ready(self):
        from apps.accounts import signals
