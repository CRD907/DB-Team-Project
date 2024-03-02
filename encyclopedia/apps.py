from django.apps import AppConfig


class EncyclopediaConfig(AppConfig):
    name = 'encyclopedia'

class PageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'