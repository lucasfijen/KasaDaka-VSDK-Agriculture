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

# from .product import Product
# from .region import Region
# from .voicelabel import VoiceLabel
from ..models import *


class Offer(models.Model):
    _urls_name = 'service-development:offer'

    class Meta:
        verbose_name = _('Offer Element')

    def __str__(self):
        return str(self.name)

    def is_active(self):
        return self.enddate >= timezone.now().date()

    def create_enddate(self):
        self.enddate = self.startdate + datetime.timedelta(days=31)

    is_active.admin_order_field = 'is_active'
    is_active.boolean = True
    is_active.short_description = 'Is active?'

    name = models.CharField(max_length = 255, null = True, blank = True)

    startdate = models.DateField(auto_now_add = True)
    enddate = models.DateField()

    # Reference to the wav that describes the product, for now redirects to voicelabel
    voice_label = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label'),
            on_delete = models.SET_NULL,
            null = True,
            blank=True,
            )

    # Reference to the recorded audio file, kept the upper one for spare
    audio_file = models.ForeignKey(
            SpokenUserInput,
            verbose_name = _('Recorded audio'),
            on_delete = models.PROTECT,
            null=True,
            blank=True,
            )

    # Selects product type
    product_type = models.ForeignKey(
            Product,
            verbose_name = _('Product type'),
            on_delete = models.SET_NULL,
            null = True,
            blank=True,
            )

    # ID towards the location field
    region = models.ForeignKey(
            Region,
            verbose_name = _('Region'),
            on_delete = models.SET_NULL,
            null = True,
            blank=True,
            )

    # Id to which user the offer belongs, gives information on phonenumber
    user_id = models.ForeignKey(
            KasaDakaUser,
            verbose_name = _('Caller id'),
            on_delete = models.CASCADE,
            null = True,
            blank=True,
            )
    # Reference to in which language the offer was recorded (we only show those in
    # the same language as the placed order)
    language = models.ForeignKey(
            Language,
            verbose_name = _('Offer_language'),
            on_delete = models.SET_NULL,
            null=True,
            blank=True,
    )