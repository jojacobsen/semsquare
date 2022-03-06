from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CalculatorConfig(AppConfig):
    name = "semsquare.calculator"
    verbose_name = _("Calculator")

    def ready(self):
        try:
            import semsquare.calculator.signals  # noqa F401
        except ImportError:
            pass
