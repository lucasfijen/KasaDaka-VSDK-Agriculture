from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from . import KasaDakaUser
from . import VoiceService, VoiceServiceElement
from . import Language
from .voicelabel import VoiceLabel


class Region(models.Model):
    _urls_name = 'service-development:region'

    class Meta:
        verbose_name = _('Region Element')

    def __str__(self):
        return str(self.region_name)

    # Reference to the wav that describes the product 
    region_name = models.CharField(max_length = 255)
    voice_label = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            )