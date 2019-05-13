from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *

def create_requests(session):
    # language = session.language
    # product = session._product
    # region = session._region
    language = get_object_or_404(Language, pk=2)
    product = 1
    region = 1
    offers = get_list_or_404(Offer, region = region, product_type = product)
    print(len(offers))
    context = { 'offers': offers,
                'questions': ['These are the offers of',
                             'pruduct',
                             'in',
                             'region'],
                'voice_labels': [offer.voice_label.get_voice_fragment_url(language) for offer in offers],
                'language': language,
                'choice_options_redirect_urls': ['vxml/offer_redirect/' + str(offer.id)  for offer in offers]
                }
    return context

def offer(request, element_id, session_id):

    session = get_object_or_404(CallSession, pk=session_id)
    # session.record_step(offer_element)

    # offers = get_list_or_404(Offer, region = 1, product_type = 1)
    # print(offers[0].user_id)
    # print(Offer.objects.filter(region = session.region, 
    #                            product_type = session.product))
    # raise Http404("Debugging")
    
    context = create_requests(session)
    
    return render(request, 'offer.xml', context, content_type='text/xml')
