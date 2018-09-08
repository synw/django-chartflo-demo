from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete


class TimeseriesConfig(AppConfig):
    name = 'timeseries'
    
    def ready(self):
        from .signals import serie_create_update, serie_delete
        from .models import Serie
        post_save.connect(serie_create_update, sender=Serie)
        post_delete.connect(serie_delete, sender=Serie)
        
