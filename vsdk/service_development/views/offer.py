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
                'choice_options_redirect_urls': ['vxml/offer_redirect/' + str(offer.id)  for offer in offers]
                }
    return context

def offer(request, element_id, session_id):

    session = get_object_or_404(CallSession, pk=session_id)
    # session.record_step(offer_element)
    
    context = create_requests(session)
    
    return render(request, 'offer.xml', context, content_type='text/xml')
