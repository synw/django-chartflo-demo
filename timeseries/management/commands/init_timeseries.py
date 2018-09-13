# -*- coding: utf-8 -*-
# @PydevCodeAnalysisIgnore
from __future__ import print_function
import random
from django.core.management.base import BaseCommand
from django.db.models.signals import post_save, post_delete
from timeseries.signals import serie_create_update, serie_delete
import pandas as pd
import numpy as np
from dataswim import ds
from chartflo.models import Dashboard, DashboardView
from timeseries.models import Serie
from timeseries.pipeline import generate


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Initialize timeseries app
        """
        post_save.disconnect(serie_create_update, sender=Serie)
        post_delete.disconnect(serie_delete, sender=Serie)
        ds.start("Creating timeseries")
        dates = list(pd.date_range(start="08/01/2018", periods=100))
        vals = np.arange(10, 150, 10)
        i = 0
        while i < 200:
            s = Serie.objects.create(
                    date=random.choice(dates),
                    value=random.choice(vals))
            print(str(i), s)
            i += 1
        ds.end("Timeseries created")
        print("Creating timeseries dashboard")
        dash, _ = Dashboard.objects.get_or_create(slug="timeseries", title="Timeseries",
                                        public=True,)
        DashboardView.objects.create(dashboard=dash, slug="rawdata", title="Raw data")
        DashboardView.objects.create(dashboard=dash, slug="day", title="Day", active=True)
        DashboardView.objects.create(dashboard=dash, slug="week", title="Week")
        DashboardView.objects.create(dashboard=dash, slug="month", title="Month")
        query = Serie.objects.all()
        generate(query)
        post_save.connect(serie_create_update, sender=Serie)
        post_delete.connect(serie_delete, sender=Serie)
        ds.ok("Finished")
