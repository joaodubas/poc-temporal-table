# encoding: utf-8
from django.db import models
from django.utils.text import slugify

from common.models import Common
from core import const


class Ledger(Common):
    CATEGORY_CHOICES = const.LEDGER_CATEGORY_CHOICES

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, db_index=True)
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subaccounts'
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Event(Common):
    effective = models.DateField(db_index=True)
    source_id = models.IntegerField()
    source_category = models.SlugField()

    class Meta:
        unique_together = ('source_id', 'source_category')


class Entry(Common):
    event = models.ForeignKey(Event, related_name='entries')
    debited = models.ForeignKey(Ledger, related_name='debits')
    credited = models.ForeignKey(Ledger, related_name='credits')
    effective = models.DateField(db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.effective = self.event.effective
        super().save(*args, **kwargs)
