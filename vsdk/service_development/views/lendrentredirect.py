from ..models import *
from django.shortcuts import *


def lendrentredirect(request, session_id):
    session = get_object_or_404(CallSession, pk=session_id)

    if session._lending:
        return HttpResponseRedirect(reverse( 'service-development:offers', kwargs= {'session_id':session.id}))
    else:
        return HttpResponseRedirect(reverse( 'service-development:offers', kwargs= {'session_id':session.id}))