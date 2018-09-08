# -*- coding: utf-8 -*-
from __future__ import print_function
import django_rq
from .models import Serie
from .pipeline import generate


def serie_create_update(sender, instance, created, **kwargs):
    query = Serie.objects.all()
    django_rq.enqueue(generate, query)


def serie_delete(sender, instance, **kwargs):
    query = Serie.objects.all()
    django_rq.enqueue(generate, query)
