from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *

def create_requests(session):
    # language = session.language
    # product = session._product
    # region = session._region
    language = get_object_or_404(Language, pk=2)
    product = get_object_or_404(Product, pk=1)
    region = get_object_or_404(Region, pk=1)
    offers = get_list_or_404(Offer, region = region, product_type = product)
    offers = [offer for offer in offers if offer.is_active()]
    questions = [get_object_or_404(VoiceLabel, name='pre_offers'), \
                product.voice_label, \
                get_object_or_404(VoiceLabel, name='post_offers'), \
                region.voice_label]
    context = { 'offers': offers,
                'questions': [question.get_voice_fragment_url(language) for question in questions],
                'voice_labels': [offer.voice_label.get_voice_fragment_url(language) for offer in offers],
                'language': language,
                'choice_options_redirect_urls': ['vxml/show_offer/' + str(session.id) + '/' + str(offer.id)  for offer in offers]
                }
    return context

def offer(request, session_id):

    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(None, 'Showed the offers')
    
    context = create_requests(session)
    
    return render(request, 'offer.xml', context, content_type='text/xml')


def show_offer(request, session_id, offer_id):

    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(None, 'Showing offer %s' % offer_id)
    offer = get_object_or_404(Offer, pk=offer_id)

    context  = {'pre_offer_voice': get_object_or_404(VoiceLabel, name='pre_offer_voice').get_voice_gragment_url(language),
                'number': ['listofnumbers'],
                'post_offer_voice': get_object_or_404(VoiceLabel, name='post_offer_voice').get_voice_gragment_url(language),
                }

    return render(request, 'show_offer.xml', context, content_type='text/xml')