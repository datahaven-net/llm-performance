from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'llm_performance'

    def ready(self):
        return True
