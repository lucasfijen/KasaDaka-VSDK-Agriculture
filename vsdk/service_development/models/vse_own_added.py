from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import reverse

from .vs_element import VoiceServiceElement, VoiceServiceSubElement

class Vse_Own_Added(VoiceServiceElement):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Own Added Elements')

    def get_absolute_url(self, session):
        """
        Returns the url at which this element is accessible through VoiceXML.
        """
        return reverse('service-development:' + str(self.name), kwargs= {'session_id':session.id})

    final_element = models.BooleanField(_('This element will terminate the call'),default = False)
    _redirect = models.ForeignKey(
            VoiceServiceElement,
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='%(app_label)s_%(class)s_related',
            verbose_name=_('Redirect element'),
            help_text = _("The element to redirect to after the message has been played."))

    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        if self._redirect :
            return VoiceServiceElement.objects.get_subclass(id = self._redirect.id)
        else: 
            return None

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def validator(self):
        errors = []
        errors.extend(super(MessagePresentation, self).validator())
        if not self.final_element and not self._redirect:
            errors.append(ugettext('Message %s does not have a redirect element and is not a final element')%self.name)
        elif not self.final_element:
            if self._redirect.id == self.id:
                errors.append(ugettext('There is a loop in %s')%str(self))
                
        return errors
