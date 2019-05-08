from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from . import KasaDakaUser
from . import VoiceService, VoiceServiceElement
from . import Language

import datetime
from django.utils import timezone


class Offer(models.Model):
    _urls_name = 'service-development:offer'

    class Meta:
        verbose_name = _('Offer Element')

    def __str__(self):
        return str(self.product_type) + str(self.region)

    def is_active(self):
        return self.enddate >= timezone.now().date()
    is_active.admin_order_field = 'is_active'
    is_active.boolean = True
    is_active.short_description = 'Is active?'


    # Reference to the wav that describes the product 
    description = models.IntegerField()

    startdate = models.DateField(auto_now_add=True)
    enddate = models.DateField()

    product_type = models.IntegerField()
    # ID towards the location field
    region = models.IntegerField()
    phonenumber = models.IntegerField()

