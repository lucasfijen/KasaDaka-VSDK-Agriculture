from ..models import *
from django.shortcuts import *


def lendrentredirect(request, session_id):
    session = get_object_or_404(CallSession, pk=session_id)
    vse_element = get_object_or_404(Vse_Own_Added, name='lendorrentredirect')
    if session._lending:
        # Goes to offers, where user will hear offers
        return HttpResponseRedirect(reverse( 'service-development:offers', kwargs= {'session_id':session.id}))
    else:
        # Goes to place to record audio and place the offer
        return HttpResponseRedirect(vse_element.redirect.get_absolute_url(session=session))