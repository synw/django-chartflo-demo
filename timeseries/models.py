# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_pandas.managers import DataFrameManager


class Serie(models.Model):
    date = models.DateField(verbose_name=_("Date"))
    value = models.FloatField(verbose_name=_("Value"))
    objects = DataFrameManager()

    class Meta:
        ordering = ("-date",)
        verbose_name = _("Serie")
        verbose_name_plural = _("Series")
        
    def __str__(self):
        return str(self.date) + " " + str(self.value)
