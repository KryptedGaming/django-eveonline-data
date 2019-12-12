from django.apps import AppConfig


class DjangoEveOnlineEntityExtensionsConfig(AppConfig):
    name = 'django_eveonline_entity_extensions'
    verbose_name = 'EVE Online Audit'
    url_slug = 'eveonline'

    def ready(self):
        from django.db.models.signals import m2m_changed, pre_delete, post_save
        from .signals import user_token_update
        from django_eveonline_connector.models import EveCharacter
        post_save.connect(user_token_update, sender=EveCharacter)