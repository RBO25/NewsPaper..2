from django.apps import AppConfig


class SimpleappnewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Category'

    def ready(self):
        import simpleappnews.signals
