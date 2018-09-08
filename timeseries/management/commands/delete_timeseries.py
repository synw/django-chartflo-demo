# -*- coding: utf-8 -*-
# @PydevCodeAnalysisIgnore
from __future__ import print_function
from django.core.management.base import BaseCommand
from django.db.models.signals import post_save, post_delete
from timeseries.signals import serie_create_update, serie_delete
from dataswim import ds
from timeseries.models import Serie


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Delete all timeseries: used for dev
        """
        post_save.disconnect(serie_create_update, sender=Serie)
        post_delete.disconnect(serie_delete, sender=Serie)
        ds.start("Deleting series")
        for s in Serie.objects.all():
            print(s)
            s.delete()
        ds.end("Series deleted")
        post_save.connect(serie_create_update, sender=Serie)
        post_delete.connect(serie_delete, sender=Serie)
        ds.ok("Finished")
