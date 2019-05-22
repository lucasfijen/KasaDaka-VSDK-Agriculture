from ..models import *
from django.shortcuts import *

def offerplacing(request, session_id):
    session = get_object_or_404(CallSession, pk=session_id)
    newoffer = Offer(product_type = session._product,
                     region = session._region,
                     user_id = session.user,
                     language = session.language)
    try:
        recording = get_object_or_404(SpokenUserInput, session = session)
        newoffer.audio_file = recording
    except:
        print('audiorecording went wrong')
        pass
    newoffer.save()
    newoffer.create_enddate()
    newoffer.save()
    final_audio_url = get_object_or_404(VoiceLabel, name='save_recording').get_voice_fragment_url(session.language)
    context = {'final_message': final_audio_url}
    render(request, 'product_selection.xml', context, content_type='text/xml')