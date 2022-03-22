from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _



class MyAppConfig(AppConfig):
    name = 'app'
    verbose_name = _("App")

    def ready(self):
        try:
            import app.signals  # noqa F401
        except ImportError:
            pass


