from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *

def create_requests(session):
    language = session._language
    product = session._product
    region = session._region
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
                'choice_options_redirect_urls': ['/vxml/show_offer/' + str(session.id) + '/' + str(offer.id)  for offer in offers]
                }
    return context

def offer(request, session_id):
    """ Page to show the offers given the product and region,
        someone selected earlier
        """
    session = get_object_or_404(CallSession, pk=session_id)
    context = create_requests(session)
    return render(request, 'offer.xml', context, content_type='text/xml')

def number_to_url_list(language, number):
    numberurls = language.get_interface_numbers_voice_label_url_list
    number = str(number)
    return [numberurls[int(n)] for n in number]

def show_offer(request, session_id, offer_id):
    """ Page to return the phone number and redirect"""
    session = get_object_or_404(CallSession, pk=session_id)

    offer = get_object_or_404(Offer, pk=offer_id)
    language = session._language
    number = session.caller_id
    
    context  = {'pre_offer_voice': get_object_or_404(VoiceLabel, name='pre_offer_voice').get_voice_fragment_url(language),
                'number': number_to_url_list(language, number),
                'post_offer_voice': get_object_or_404(VoiceLabel, name='post_offer_voice').get_voice_fragment_url(language),
                }

    return render(request, 'show_offer.xml', context, content_type='text/xml')