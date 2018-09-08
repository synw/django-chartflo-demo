# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Serie


@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'value',
    )
    list_filter = ('date',)
    date_hierarchy = 'date'
