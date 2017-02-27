# encoding: utf-8
from django.contrib.postgres import fields
from django.db import models


class Timestamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MetaInfo(models.Model):
    metadata = fields.JSONField(default={})

    class Meta:
        abstract = True


class Note(models.Model):
    note = models.TextField(default='')

    class Meta:
        abstract = True


class Common(Timestamp, MetaInfo, Note):
    def __str__(self):
        return '{0.__class__.__name__} #{0.pk}'.format(self)

    class Meta:
        abstract = True
