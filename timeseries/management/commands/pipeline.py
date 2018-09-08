# -*- coding: utf-8 -*-
from __future__ import print_function
from django.core.management.base import BaseCommand
from django.db.models.signals import post_save, post_delete
from timeseries.signals import serie_create_update, serie_delete
from timeseries.models import Serie
from timeseries.pipeline import generate


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Run the data pipeline
        """
        post_save.disconnect(serie_create_update, sender=Serie)
        post_delete.disconnect(serie_delete, sender=Serie)
        query = Serie.objects.all()
        generate(query)
        post_save.connect(serie_create_update, sender=Serie)
        post_delete.connect(serie_delete, sender=Serie)
