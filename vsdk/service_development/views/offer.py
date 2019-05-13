from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *


def offer_options_resolve_redirect_urls(offer_options, session):
    offer_options_redirection_urls = []
    for offer_option in offer_options:
        redirect_url = offer_option.redirect.get_absolute_url(session)
        offer_options_redirection_urls.append(redirect_url)
    return offer_options_redirection_urls

def offer_options_resolve_voice_labels(offer_options, language):
    """
    Returns a list of voice labels belonging to the provided list of offer_options.
    """
    offer_options_voice_labels = []
    for offer_option in offer_options:
        offer_options_voice_labels.append(offer_option.get_voice_fragment_url(language))
    return offer_options_voice_labels

def offer_generate_context(offer_element, session):
    """
    Returns a dict that can be used to generate the offer VXML template
    offer = this offer element object
    offer_voice_label = the resolved Voice Label URL for this offer element
    offer_options = iterable of offerOption object belonging to this offer element
    offer_options_voice_labels = list of resolved Voice Label URL's referencing to the offer_options in the same position
    offer_options_redirect_urls = list of resolved redirection URL's referencing to the offer_options in the same position
        """
    language = session.language
    product = session.product
    region = session.region
    offer_options =  offer_element.all()
    context = { 'offer':offer_element,
                'offer_voice_label':offer_element.get_voice_fragment_url(language),
                'offer_options': offer_options,
                'offer_options_voice_labels':offer_options_resolve_voice_labels(offer_options, language),
                'offer_options_redirect_urls': offer_options_resolve_redirect_urls(offer_options,session),
                'language': language,
                }
    return context

def offer(request, element_id, session_id):

    session = get_object_or_404(CallSession, pk=session_id)
    # session.record_step(offer_element)
    offers = get_list_or_404(Offer, region = 1, product_type = 1)
    print(offers[0].user_id)
    print(Offer.objects.filter(region = session.region, 
                               product_type = session.product))
    raise Http404("Debugging")
    
    # context = offer_generate_context(offer_element, session)
    
    # return render(request, 'offer.xml', context, content_type='text/xml')

