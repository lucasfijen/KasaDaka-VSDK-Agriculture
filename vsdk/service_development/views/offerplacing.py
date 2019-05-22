from ..models import *
from django.shortcuts import *

def offerplacing(request, session_id):
    session = get_object_or_404(CallSession, pk=session_id)
    # Offer(models.Model)