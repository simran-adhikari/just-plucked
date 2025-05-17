from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order'
    def ready(self):
        # import the signals module to register handlers
        import order.signals
